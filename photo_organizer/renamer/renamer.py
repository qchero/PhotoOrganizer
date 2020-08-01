from pathlib import Path


class Renamer:

    def __init__(self, time_extractors):
        self.time_extractors = time_extractors
        self.file_path_pattern = "./%Y/%m/%Y%m%d_%H%M%S"
        pass

    def get_path(self, path: Path) -> Path:
        """
        Get the new path for a file with time extracted from the file
        @param path: File path
        @return: The new file name
        """
        path = Path(path)
        filename = path.name
        for time_extractor in self.time_extractors:
            time = time_extractor.get_time(filename)
            if time is not None:
                new_file_name = time.strftime(self.file_path_pattern)
                return Path(new_file_name + path.suffix)

        raise Exception(f"Failed to infer time for {path}")

    @staticmethod
    def suffix_path(path: Path, suffix: int) -> Path:
        """
        Suffix the path for avoiding name confliction
        @param path: file path
        @param suffix: the suffix number
        @return: new path
        """
        if suffix > 99:
            raise Exception(f"Suffix is more than 2 digit")

        return path.parent / (path.stem + f"_{suffix:02}") / path.suffix
