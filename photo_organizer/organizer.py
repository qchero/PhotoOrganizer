import glob
import logging
import os

from .cache import Cache
from .config import Config
from .hasher import get_hash


class Organizer:

    def __init__(self, config: Config):
        """
        Constructor
        """
        logging.debug(f"Setting up Organizer")
        self.config = config
        self.cache = Cache(self.config.working_dir)

    def setup(self):
        """
        Set up the Organizer library:
        1. For all files in the LibraryDir, calculate the MD5 and store it in Cache
        2. For all docs in Cache, remove if the file no longer exists
        """
        logging.debug(f"Running setup command")
        glob_path = os.path.join(self.config.library_dir, "**/*.mp4")
        for file_path in glob.glob(glob_path, recursive=True):
            file_abspath = os.path.abspath(file_path)
            if file_abspath.startswith(os.path.abspath(self.config.incoming_dir)):
                logging.debug(f"Ignore IncomingDir: {file_abspath}")
                continue
            if any([file_abspath.startswith(os.path.abspath(dir_path)) for dir_path in self.config.library_ignore_dirs]):
                logging.debug(f"Ignore IgnoreDirs: {file_abspath} ")
                continue

            existing_doc = self.cache.get_doc_by_path(file_abspath)
            if existing_doc is not None:
                if existing_doc["size"] == os.path.getsize(file_abspath):
                    logging.debug(f"Hash exists {existing_doc['hashcode']}: {file_abspath}")
                    continue
                else:
                    logging.info(f"File size changed after organized: {file_abspath}")

            md5 = get_hash(file_abspath, size_threshold=self.config.md5_size_limit * 1024 * 1024)
            self.cache.upsert_hashcode_doc(file_abspath, md5, os.path.getsize(file_abspath))
            logging.debug(f"Hashed to {md5}: {file_abspath}")
