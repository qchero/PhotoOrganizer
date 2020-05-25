import logging
import os

from .cache import Cache
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

    def analyze(self):
        """
        Scan for duplicates which are harmless but annoying:
        - Multiple files with the same hash
        - Multiple files with the same name
        """
        all_docs = self.cache.get_all()
        # for doc in all_docs:
        #     if doc.hashcode.isdigit():
        #         self.cache.delete_by_path(doc.path)
        for hashcode in set([doc.hashcode for doc in all_docs]):
            docs = self.cache.get_docs_by_hashcode(hashcode)
            if len(docs) > 1:
                logging.warning(f"Duplicate files found with MD5 {hashcode}: {[doc.path for doc in docs]}")

        file_name_to_doc = self._group_by_file_name(all_docs)
        for file_name, docs in file_name_to_doc.items():
            if len(docs) > 1:
                logging.warning(f"Duplicate files with the same name found: {[doc.path for doc in docs]}")

    def rename(self):
        """
        Rename
        """
        self.setup()

    def setup(self):
        """
        Set up the Organizer library:
        1. For all docs in Cache, remove if the file no longer exists
        2. For all files in the LibraryDir, calculate the hash and store it in Cache
        """
        self._remove_redundant_hash()

        media_paths = self.library.get_all_library_paths()
        self._pave_cache(media_paths)

        logging.info("Setup Summary:")
        self.counter_logger.dump()

    def _remove_redundant_hash(self):
        for path in [doc.path for doc in self.cache.get_all()]:
            if not os.path.exists(path):
                self.cache.delete_by_path(path)
                logging.debug(f"Hash removed for non-exist file: {path}")
                self.counter_logger.inc("Hash removed")

    def _pave_cache(self, media_paths):
        for file_path in media_paths:
            # Check if cache entry already exists
            existing_doc = self.cache.get_doc_by_path(file_path)
            if existing_doc is not None:
                if existing_doc.size == os.path.getsize(file_path):
                    logging.debug(f"Hash exists {existing_doc.hashcode}: {file_path}")
                    self.counter_logger.inc("Hash exists", step=10000)
                    continue
                logging.info(f"File size changed after organized, rehashing: {file_path}")

            # Compute and update hash
            md5 = get_hash(file_path, self.config.md5_size_limit * 1024 * 1024)
            self.cache.upsert_hashcode_doc(file_path, md5, os.path.getsize(file_path))
            logging.debug(f"Hashed to {md5}: {file_path}")
            self.counter_logger.inc("Hash computed")

    @staticmethod
    def _group_by_file_name(docs):
        file_name_to_doc = {}
        for doc in docs:
            file_name = os.path.basename(doc.path).lower()
            if file_name not in file_name_to_doc[file_name]:
                file_name_to_doc[file_name] = []
            file_name_to_doc[file_name].append(doc)
        return file_name_to_doc
