import logging
import os
from pathlib import Path
from typing import List

from photo_organizer.config import Config


class Library:

    def __init__(self, config: Config):
        self._config = config

    def get_all_library_paths(self) -> List[Path]:
        """
        Get all the media paths in the library
        @return: Paths that are relative to LibraryDir and all lowercase
        """
        glob_paths = self._config.cur_working_dir.glob("[0-9]*/**/*")
        return list(filter(lambda p: self._is_media_path(p), glob_paths))

    def get_all_incoming_paths(self) -> List[Path]:
        """
        Get all the media paths in the incoming dir
        @return: Paths that are relative to incoming dir and all lowercase
        """
        glob_paths = self._config.incoming_dir.glob("**/*")
        return list(filter(lambda p: self._is_media_path(p), glob_paths))

    @staticmethod
    def move_file(cur_path: Path, new_path: Path):
        """
        Move file from current path to new path inside the library
        """
        new_path.parent.mkdir(parents=True, exist_ok=True)
        if new_path.exists():
            raise Exception(f"Attempt to overwrite {new_path}!")
        cur_path.rename(new_path)

    @staticmethod
    def _is_media_path(path: Path):
        suffix = path.suffix.lower()
        if suffix == "":
            return False
        elif suffix not in [".bmp", ".gif", ".heic", ".jpg", ".jpeg", ".m4v", ".mov", ".mp4",
                            ".nef", ".png"]:
            logging.info(f"Not a recognized media file: {path}")
            return False
        else:
            return True
