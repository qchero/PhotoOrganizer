from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

import pytest

from photo_organizer.renamer.renamer import Renamer


class TestRenamer:
    def test_get_path(self):
        extractor = Mock()
        extractor.get_time = Mock(return_value=datetime(2020, 8, 1, 9, 36, 50))
        renamer = Renamer([extractor])

        assert renamer.get_path(Path("./dir1/dir2/1.jpg")) == Path("2020/08/20200801_093650.jpg")
        assert renamer.get_path(Path("1.jpg")) == Path("2020/08/20200801_093650.jpg")

        extractor.get_time = Mock(return_value=None)
        with pytest.raises(Exception):
            renamer.get_path(Path("1.jpg"))

    def test_suffix_path(self):
        renamer = Renamer([])
        assert renamer.suffix_path(Path("./dir1/dir2/1.jpg"), 1) == Path("./dir1/dir2/1_01.jpg")
        assert renamer.suffix_path(Path("666.mp4"), 50) == Path("666_50.mp4")

        with pytest.raises(Exception):
            renamer.suffix_path(Path("666.mp4"), 100)
