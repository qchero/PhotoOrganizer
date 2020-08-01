import datetime
import re
import logging


class FileNameTimeExtractor:
    """
    The naming strategy by inferring from file name
    """

    def __init__(self):
        self.known_patterns = [
            "%Y%m%d_%H%M%S"
        ]

    def get_time(self, filename):
        for pattern in self.known_patterns:
            regex_pattern = self._get_regex_pattern(pattern)
            matches = re.findall(regex_pattern, filename)
            if len(matches) == 0:
                continue
            elif len(matches) > 1:
                logging.warning(f"Multiple time pattern matches in the file name: {filename}")
                continue

            return datetime.datetime.strptime(matches[0], pattern)

        return None

    @staticmethod
    def _get_regex_pattern(time_pattern):
        regex_pattern = time_pattern.replace("%", "")
        regex_pattern = re.sub("[mMdDhHsS]", "\\\\d\\\\d", regex_pattern)
        regex_pattern = re.sub("[yY]", "\\\\d\\\\d\\\\d\\\\d", regex_pattern)
        return regex_pattern
