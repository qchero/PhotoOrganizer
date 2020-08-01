import logging
import os
from typing import List, Callable

from exception.exception import AuditException
from .cache import Cache, Doc
from .config import Config
from .hasher import Hasher
from .library import Library
from .logging.counter import CounterLogger
from .renamer.renamer import Renamer
from .renamer.time_extractor import FileNameTimeExtractor


class Organizer:

    def __init__(self, config: Config):
        """
        Constructor
        """
        self.config = config
        self.cache = Cache(self.config)
        self.hasher = Hasher(self.config.md5_size_limit * 1024 * 1024)
        self.library = Library(self.config)
        self.counter_logger = CounterLogger()
        self.renamer = Renamer([FileNameTimeExtractor()])

    def audit(self):
        """
        Scan for duplicates which are harmless but annoying:
        1. Multiple files with the same hash
        2. Multiple files with the same name
        3. File modification after hashing found by size change
        """
        audit_issue_found = False
        all_docs = self.cache.get_all()
        cache_hash_to_docs = self._group_by(self.cache.get_all(), lambda doc: doc.hashcode)
        for hashcode, docs in cache_hash_to_docs.items():
            if len(docs) > 1:
                logging.warning(f"Duplicate files with same hash {hashcode}: {[doc.path for doc in docs]}")
                audit_issue_found = True

        file_name_to_docs = self._group_by(all_docs, lambda d: os.path.basename(d.path).lower())
        for file_name, docs in file_name_to_docs.items():
            if len(docs) > 1:
                logging.warning(f"Duplicate files with the same name found: {[doc.path for doc in docs]}")
                audit_issue_found = True

        for doc in all_docs:
            if os.path.getsize(doc.path) != doc.size:
                logging.warning(f"File size changed after hashing: {doc.path}")
                audit_issue_found = True

        logging.info("Audit completed!")
        if audit_issue_found:
            raise AuditException()

    def merge(self, preview: bool):
        """
        Merge the photos pending processing into the library
        0. Run setup
        1. Find out the duplicated ones and exclude those
        2. Rename files according to the file info
        3. If not preview, move the files and update cache
        """
        self.setup()

        incoming_paths = sorted(self.library.get_all_incoming_paths())
        logging.info(f"Process incoming files: {len(incoming_paths)}")

        incoming_path_to_hash = {}
        incoming_hash_to_path = {}
        incoming_path_to_new_path = {}
        library_dedup_paths = set(self.library.get_all_library_paths())
        for path in incoming_paths:
            # Deduplication
            hashcode = self.hasher.get_hash(path)
            if hashcode in incoming_hash_to_path:
                logging.warning(f"Duplicate: {path} == {incoming_hash_to_path[hashcode]}")
                self.counter_logger.inc("Duplicates")
                continue
            same_hash_files = self.cache.get_docs_by_hashcode(hashcode)
            if len(same_hash_files) > 0:
                logging.warning(f"Duplicate: {path} == {same_hash_files[0].path}")
                self.counter_logger.inc("Duplicates")
                continue

            incoming_hash_to_path[hashcode] = path
            incoming_path_to_hash[path] = hashcode

            # Calculate new paths
            dedup_suffix = 0
            new_path = self.renamer.get_path(path)
            while new_path in library_dedup_paths:
                dedup_suffix = dedup_suffix + 1
                new_path = self.renamer.suffix_path(path, dedup_suffix)

            logging.info(f"Plan to move {path} => {new_path}")
            incoming_path_to_new_path[path] = new_path
            library_dedup_paths.add(new_path)

        if preview:
            logging.info("Abort for preview")
            return

        for cur_path, new_path in incoming_path_to_new_path.items():
            logging.info(f"Move {cur_path} => {new_path}")
            self.library.move_file(cur_path, new_path)
            self.cache.upsert_hashcode_doc(new_path, incoming_path_to_hash[cur_path], os.path.getsize(new_path))
            self.counter_logger.inc("Added to library")

        self.counter_logger.dump()

    def setup(self):
        """
        Set up the Organizer library:
        1. For all docs in Cache, remove if the file is missing in Library
        2. For all files in the Library, hash it if the hash is missing in Cache
        """
        library_paths = set(self.library.get_all_library_paths())
        cache_docs = self.cache.get_all()
        self._setup_remove_redundant_hash(library_paths, cache_docs)

        cache_docs = self.cache.get_all()
        self._setup_pave_cache(library_paths, cache_docs)

        self.counter_logger.dump()

    def _setup_remove_redundant_hash(self, library_paths, cache_docs):
        for path in [doc.path for doc in cache_docs]:
            if path not in library_paths:
                self.cache.delete_by_path(path)
                logging.debug(f"Hash removed for non-exist file: {path}")
                self.counter_logger.inc("Hash removed", step=1000)

    def _setup_pave_cache(self, library_paths, cache_docs):
        # Check if cache entry already exists
        cache_paths = set([doc.path for doc in cache_docs])
        paths_to_hash = list(filter(lambda p: p not in cache_paths, library_paths))
        self.counter_logger.inc(f"Hash exists", increment=len(library_paths) - len(paths_to_hash))

        # Compute and update hash
        logging.info(f"Files to hash: {len(paths_to_hash)}")
        for path in paths_to_hash:
            hashcode = self.hasher.get_hash(path)
            self.cache.upsert_hashcode_doc(path, hashcode, os.path.getsize(path))
            logging.debug(f"Hashed to {hashcode}: {path}")
            self.counter_logger.inc("Hash computed", step=1000)

    @staticmethod
    def _group_by(docs: List[Doc], key_selector: Callable[[Doc], str]):
        key_to_doc = {}
        for doc in docs:
            key = key_selector(doc)
            if key not in key_to_doc:
                key_to_doc[key] = []
            key_to_doc[key].append(doc)
        return key_to_doc
