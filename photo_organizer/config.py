import json
import logging
import os

from exception.exception import InvalidConfigException


class Config:

    def __init__(self):
        """
        Create a Config by parsing the config.json file under current working dir.
        library_dir - The directory of the organized media library
        incoming_dir - The directory of the incoming medias
        working_dir - The directory of dbs, logs and other temporary files
        md5_size_limit -
        """
        logging.debug(f"Setting up Config")
        cur_working_dir = os.getcwd()
        config_file_path = os.path.join(cur_working_dir, "config.json")
        if not os.path.exists(config_file_path):
            raise InvalidConfigException(f"Config file not found at {config_file_path}")

        with open(config_file_path, "r") as config_file:
            config = json.loads(config_file.read())

        self.library_dir = self._get_or_default(config, "LibraryDir", cur_working_dir)
        self._validate_dir_exists(self.library_dir, "LibraryDir")

        self.library_ignore_dirs = self._get_or_default(config, "LibraryIgnoreDirs", [])

        self.incoming_dir = self._get_or_raise(config, "IncomingDir")
        self._validate_dir_exists(self.incoming_dir, "IncomingDir")

        self.working_dir = self._get_or_default(config, "WorkingDir",
                                                os.path.join(self.library_dir, ".PhotoOrganizer/"))
        os.makedirs(self.working_dir, exist_ok=True)

        self.md5_size_limit = 100

        logging.debug(f"Config: {json.dumps(self, default=lambda x: x.__dict__)}")

    @staticmethod
    def _validate_dir_exists(dir_path, dir_name):
        if not os.path.exists(dir_path):
            raise InvalidConfigException(f"{dir_name} directory {dir_path} does not exists")

    @staticmethod
    def _get_or_default(config, key, default):
        if key not in config:
            return default
        return config[key]

    @staticmethod
    def _get_or_raise(config, key):
        if key not in config:
            raise InvalidConfigException(f"{key} Not found in config.json")
        return config[key]
