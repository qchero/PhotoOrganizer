import json
import logging
from pathlib import Path

from exception.exception import InvalidConfigException


class Config:

    def __init__(self):
        """
        Create a Config by parsing the config.json file under current working dir.
        cur_working_dir - The current working dir where the script is run
        incoming_dir - The directory of the incoming medias
        working_dir - The directory of dbs, logs and other temporary files
        """
        self.cur_working_dir = Path(".")
        config_file_path = self.cur_working_dir / "config.json"
        if not config_file_path.exists():
            raise InvalidConfigException(f"Config file not found at {config_file_path}")
        with config_file_path.open("r") as config_file:
            config = json.loads(config_file.read())

        self.incoming_dir = self.cur_working_dir / self._get_or_raise(config, "IncomingDir")
        self._validate_dir_exists(self.incoming_dir, "IncomingDir")

        self.working_dir = self.cur_working_dir / ".PhotoOrganizer"
        if not self.working_dir.exists():
            self.working_dir.mkdir(parents=True, exist_ok=True)

        self.md5_size_limit = 100

        logging.debug(f"Config: {config}")

    @staticmethod
    def _validate_dir_exists(dir_path, dir_name):
        if not dir_path.exists():
            raise InvalidConfigException(f"{dir_name} directory {dir_path} does not exists")

    @staticmethod
    def _get_or_raise(config, key):
        if key not in config:
            raise InvalidConfigException(f"{key} Not found in config.json")
        return config[key]
