import pathlib
from datetime import datetime
from unittest.mock import Mock

from photo_organizer.renamer.renamer import Renamer


class TestRenamer:
    def test_rename(self):
        extractor = Mock()
        extractor.get_time = Mock(return_value=datetime(2020, 8, 1, 9, 36, 50))
        renamer = Renamer([extractor])

        assert renamer.get_path(pathlib.Path("./dir1/dir2/1.jpg")) == pathlib.Path("2020/08/20200801_093650.jpg")
        assert renamer.get_path(pathlib.Path("1.jpg")) == pathlib.Path("2020/08/20200801_093650.jpg")
