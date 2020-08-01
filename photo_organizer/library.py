import logging
import pathlib
from typing import List

from photo_organizer.config import Config


class Library:

    def __init__(self, config: Config):
        self._config = config

    def get_all_library_paths(self) -> List[str]:
        """
        Get all the media paths in the library
        @return: Paths that are relative to LibraryDir and all lowercase
        """
        glob_paths = self._config.cur_working_dir.glob("[0-9]*/**/*")
        media_paths = list(filter(lambda p: self._is_media_path(p), glob_paths))
        return [str(p).lower() for p in media_paths]

    def get_all_incoming_paths(self) -> List[str]:
        """
        Get all the media paths in the incoming dir
        @return: Paths that are relative to incoming dir and all lowercase
        """
        glob_paths = self._config.incoming_dir.glob("[0-9]*/**/*")
        media_paths = list(filter(lambda p: self._is_media_path(p), glob_paths))
        return [str(p).lower() for p in media_paths]

    @staticmethod
    def _is_media_path(path: pathlib.Path):
        suffix = path.suffix.lower()
        if suffix == "":
            return False
        elif suffix not in [".bmp", ".gif", ".heic", ".jpg", ".jpeg", ".m4v", ".mov", ".mp4",
                            ".nef", ".png"]:
            logging.debug(f"Not a recognized media file: {path}")
            return False
        else:
            return True
