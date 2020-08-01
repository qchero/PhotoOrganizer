from datetime import datetime

import pytest

from photo_organizer.renamer.time_extractor import FileNameTimeExtractor


class TestFileNameTimeExtractor:
    @staticmethod
    @pytest.mark.parametrize("filename,expected_time", [
        ("1.jpg", None),
        ("IMG_20200801_091355.jpg", datetime(2020, 8, 1, 9, 13, 55)),
        ("VID_20200801_091355_9394.jpg", datetime(2020, 8, 1, 9, 13, 55)),
        ("VID_20200801_202008_20200801_091310.jpg", None)
    ])
    def test_get_time_should_extract_correctly(filename, expected_time):
        extractor = FileNameTimeExtractor()
        assert extractor.get_time(filename) == expected_time
