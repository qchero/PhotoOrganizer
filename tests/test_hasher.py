import pathlib
from pathlib import Path

import pytest

from photo_organizer.hasher import Hasher


@pytest.fixture(autouse=True)
def each_function():
    path = Path("./2020/1.jpg")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        f.write("SomeRandomContent")
    yield None


def test_should_hash_correctly():
    hasher = Hasher(100)
    hashcode = hasher.get_hash(pathlib.Path("./2020/1.jpg"))
    assert hashcode == "b539721f0afbb19451fb5e3c782e1804"

    hasher = Hasher(5)
    hashcode = hasher.get_hash(pathlib.Path("./2020/1.jpg"))
    assert hashcode == "17"
