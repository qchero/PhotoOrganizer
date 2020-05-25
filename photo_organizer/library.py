import glob
import os
import pathlib

from photo_organizer.config import Config


class Library:

    def __init__(self, config: Config):
        self.config = config

    def get_all_library_paths(self):
        glob_path = os.path.join(self.config.library_dir, "**/*")
        all_paths = [os.path.abspath(p) for p in glob.glob(glob_path, recursive=True)]
        return filter(lambda p: self._is_media_path(p) and not self._should_ignore(p), all_paths)

    @staticmethod
    def _is_media_path(path):
        return pathlib.Path(path).suffix.lower() in [".bmp", ".gif", ".heic", ".jpg", ".jpeg", ".m4v", ".mov",
                                                     ".nef", ".png"]

    def _should_ignore(self, path):
        file_abspath = os.path.abspath(path)
        if file_abspath.startswith(os.path.abspath(self.config.incoming_dir)):
            return True

        if any([file_abspath.startswith(os.path.abspath(ignore_dir_path))
                for ignore_dir_path in self.config.library_ignore_dirs]):
            return True

        return False
