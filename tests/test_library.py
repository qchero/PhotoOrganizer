import os
import shutil
from pathlib import Path
from unittest.mock import Mock

import pytest

from photo_organizer.library import Library


@pytest.fixture(autouse=True)
def each_function():
    temp_path = "./Temp/"
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path, ignore_errors=True)
    os.makedirs(temp_path, exist_ok=True)
    os.chdir(temp_path)
    yield None
    os.chdir("..")
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture()
def library():
    config = Mock()
    config.cur_working_dir = Path(".")
    yield Library(config)


class Test_get_all_library_paths:
    @staticmethod
    @pytest.mark.parametrize("paths,expected_library_paths", [
        (["./2000/1.jpg", "./2020/05/2.jpg"], ["./2000/1.jpg", "./2020/05/2.jpg"]),
        (["./2000/1.jpg", "./Random/2.jpg"], ["./2000/1.jpg"]),
        (["./2000/1.txt"], []),
        (["./2000/LOWER.jpEg"], ["./2000/lower.jpeg"])
    ], ids=[
        "file_should_be_found",
        "file_not_in_year_dir_should_be_ignored",
        "non_media_file_should_be_ignored",
        "file_should_be_lowercase"
    ])
    def test_should_hash_correctly(library, paths, expected_library_paths):
        for p in paths:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w") as f:
                f.write("RandomText")

        paths = library.get_all_library_paths()
        assert all([p.startswith("20") for p in paths])  # Should be relative path
        assert paths == [str(Path(p)) for p in expected_library_paths]
