from pathlib import Path

import pytest

from photo_organizer.hasher import get_hash


@pytest.fixture(autouse=True)
def each_function():
    path = Path("./2020/1.jpg")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        f.write("SomeRandomContent")
    yield None


def test_should_hash_correctly():
    hashcode = get_hash("./2020/1.jpg", 100)
    assert hashcode == "b539721f0afbb19451fb5e3c782e1804"

    hashcode = get_hash("./2020/1.jpg", 5)
    assert hashcode == "17"
