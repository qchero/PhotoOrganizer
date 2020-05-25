import os
import shutil

import pytest

from photo_organizer.hasher import get_hash


@pytest.fixture(autouse=True)
def each_function():
    temp_path = "./Temp/"
    os.makedirs(temp_path, exist_ok=True)
    with open("./Temp/1.jpg", "w") as f:
        f.write("SomeRandomContent")
    yield None
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path, ignore_errors=True)


def test_should_hash_correctly():
    hashcode = get_hash("./Temp/1.jpg", 100)
    assert hashcode == "b539721f0afbb19451fb5e3c782e1804"

    hashcode = get_hash("./Temp/1.jpg", 5)
    assert hashcode == "17"
