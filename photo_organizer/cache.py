import logging
import os
from typing import TypedDict, Optional, List

import sqlite3
from exception.exception import DatabaseException
from photo_organizer.config import Config


class Doc:
    def __init__(self, path, hashcode, size):
        self.path = path
        self.hashcode = hashcode
        self.size = size


class Cache:
    def __init__(self, config: Config):
        """
        Creating the cache object depending on a TinyDB file under WorkingDir
        @param config: The config
        """
        logging.debug(f"Setting up Cache")
        os.makedirs(config.working_dir, exist_ok=True)
        self._config = config
        self._conn = sqlite3.connect(os.path.join(self._config.working_dir, "database.db"), isolation_level=None)
        self._conn.execute("""CREATE TABLE IF NOT EXISTS hash (
                             path text PRIMARY KEY,
                             hashcode text NOT NULL,
                             size long NOT NULL); """)
        self._conn.execute("""CREATE INDEX IF NOT EXISTS hashcode ON hash (hashcode)""")

    def __del__(self):
        if self._conn is not None:
            self._conn.close()

    def delete_by_path(self, path: str) -> None:
        """
        Get the doc by hash
        @param path: The path
        @return: The doc
        """
        self._conn.execute(f"DELETE FROM hash WHERE path = '{self._get_path_key(path)}'")

    def get_all(self):
        rows = self._conn.execute(f"SELECT * FROM hash").fetchall()
        return [self._row_to_doc(row) for row in rows]

    def get_doc_by_path(self, path: str) -> Optional[Doc]:
        """
        Get the doc by file path
        @param path: The file path
        @return: The doc
        """
        rows = self._conn.execute(f"SELECT * FROM hash WHERE path = '{self._get_path_key(path)}'").fetchall()
        if len(rows) == 0:
            return None
        elif len(rows) > 1:
            raise DatabaseException("DB contains unexpected data! Multiple records for the same path exist!")

        return self._row_to_doc(rows[0])

    def get_docs_by_hashcode(self, hashcode: str) -> List[Doc]:
        """
        Get the doc by hash
        @param hashcode: The hashcode
        @return: The doc
        """
        rows = self._conn.execute(f"SELECT * FROM hash WHERE hashcode = '{hashcode}'").fetchall()
        return [self._row_to_doc(row) for row in rows]

    def upsert_hashcode_doc(self, path: str, hashcode: str, size: int) -> None:
        """
        Insert an record into the DB
        @param path: The file path
        @param hashcode: The MD5
        @param size: The file size
        @return: success or not
        """
        self._conn.execute(f"REPLACE INTO hash VALUES ('{self._get_path_key(path)}', '{hashcode}', {size})")

    @staticmethod
    def _row_to_doc(row):
        return Doc(row[0], row[1], row[2])

    def _get_path_key(self, path):
        return os.path.relpath(path, self._config.library_dir).lower()
