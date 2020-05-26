import logging
import os
from typing import List, Callable

from .cache import Cache, Doc
from .config import Config
from .hasher import get_hash
from .library import Library
from .logging.counter import CounterLogger


class Organizer:

    def __init__(self, config: Config):
        """
        Constructor
        """
        logging.debug(f"Setting up Organizer")
        self.config = config
        self.cache = Cache(self.config)
        self.library = Library(self.config)
        self.counter_logger = CounterLogger()

    def audit(self):
        """
        Scan for duplicates which are harmless but annoying:
        - Multiple files with the same hash
        - Multiple files with the same name
        - File modification after hashing found by size change
        """
        all_docs = self.cache.get_all()
        cache_hash_to_docs = self._group_by(self.cache.get_all(), lambda doc: doc.hashcode)
        for hashcode, docs in cache_hash_to_docs.items():
            if len(docs) > 1:
                logging.warning(f"Duplicate files with same hash {hashcode}: {[doc.path for doc in docs]}")

        file_name_to_docs = self._group_by(all_docs, lambda d: os.path.basename(d.path).lower())
        for file_name, docs in file_name_to_docs.items():
            if len(docs) > 1:
                logging.warning(f"Duplicate files with the same name found: {[doc.path for doc in docs]}")

        for doc in all_docs:
            if os.path.getsize(doc.path) != doc.size:
                logging.warning(f"File size changed after hashing: {doc.path}")

    def rename(self):
        """
        Rename
        """
        self.setup()

    def setup(self):
        """
        Set up the Organizer library:
        1. For all docs in Cache, remove if the file is missing in Library
        2. For all files in the Library, hash it if the hash is missing in Cache
        """
        library_paths = set(self.library.get_all_library_paths())
        cache_docs = self.cache.get_all()
        self._remove_redundant_hash(library_paths, cache_docs)

        cache_docs = self.cache.get_all()
        self._pave_cache(library_paths, cache_docs)

        logging.info("Setup Summary:")
        self.counter_logger.dump()

    def _remove_redundant_hash(self, library_paths, cache_docs):
        for path in [doc.path for doc in cache_docs]:
            if path not in library_paths:
                self.cache.delete_by_path(path)
                logging.debug(f"Hash removed for non-exist file: {path}")
                self.counter_logger.inc("Hash removed", step=1000)

    def _pave_cache(self, library_paths, cache_docs):
        # Check if cache entry already exists
        cache_paths = set([doc.path for doc in cache_docs])
        paths_to_hash = list(filter(lambda p: p not in cache_paths, library_paths))
        self.counter_logger.inc(f"Hash exists", increment=len(library_paths) - len(paths_to_hash))

        # Compute and update hash
        logging.info(f"Files to hash: {len(paths_to_hash)}")
        for path in paths_to_hash:
            md5 = get_hash(path, self.config.md5_size_limit * 1024 * 1024)
            self.cache.upsert_hashcode_doc(path, md5, os.path.getsize(path))
            logging.debug(f"Hashed to {md5}: {path}")
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
