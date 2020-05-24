import logging
import os

from tinydb import TinyDB, Query


class Cache:

    def __init__(self, working_dir):
        """
        Creating the cache object depending on a TinyDB file under WorkingDir
        """
        logging.debug(f"Setting up Cache")
        self.db = TinyDB(os.path.join(working_dir, "db.json"))
        self.query_doc = Query()

    def upsert_hashcode_doc(self, path, hashcode, size):
        """
        Insert an record into the DB
        @param path: The file path
        @param hashcode: The MD5
        @param size: The file size
        @return: success or not
        """
        self.db.upsert({'path': path, 'hashcode': hashcode, 'size': size}, self.query_doc.path == path)

    def get_all(self):
        return self.db.all()

    def get_doc_by_path(self, path):
        """
        Get the doc by file path
        @param path: The file path
        @return: The doc
        """
        search_result = self.db.search(self.query_doc.path == path)
        if len(search_result) == 0:
            return None
        elif len(search_result) > 1:
            raise Exception("DB contains unexpected data! Multiple records for the same path exist!")

        return search_result[0]

    def get_doc_by_hashcode(self, hashcode):
        """
        Get the doc by hash
        @param hashcode: The hashcode
        @return: The doc
        """
        search_result = self.db.search(self.query_doc.hashcode == hashcode)
        if len(search_result) == 0:
            return None
        elif len(search_result) > 1:
            raise Exception("DB contains unexpected data! Multiple records for the same MD5 exist!")

        return search_result[0]
