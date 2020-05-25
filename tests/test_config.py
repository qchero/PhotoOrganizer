import json
import os
import shutil
import pytest

from exception.exception import InvalidConfigException
from photo_organizer.config import Config


@pytest.fixture(autouse=True)
def each_function():
    temp_path = "./Temp/"
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path, ignore_errors=True)
    yield None
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture()
def setup_full_config_file():
    full_config = {
        "LibraryDir": "./Temp/LibraryDir",
        "LibraryIgnoreDirs": [
            "./Temp/NoDate",
            "./Temp/Special"
        ],
        "IncomingDir": "./Temp/IncomingDir",
        "WorkingDir": "./Temp/WorkingDir",
        "MD5SizeLimitMB": 666
    }
    with open("./config.json", "w") as config_file:
        config_file.write(json.dumps(full_config))
    os.makedirs("./Temp/IncomingDir", exist_ok=True)
    os.makedirs("./Temp/LibraryDir", exist_ok=True)
    yield None
    os.remove("./config.json")


@pytest.fixture()
def setup_minimum_config_file():
    with open("./config.json", "w") as config_file:
        config_file.write(json.dumps({
            "IncomingDir": "./Temp/IncomingDir"
        }))
    os.makedirs("./Temp/IncomingDir", exist_ok=True)
    yield None
    os.remove("./config.json")


@pytest.fixture()
def setup_missing_key_config_file():
    with open("./config.json", "w") as config_file:
        config_file.write(json.dumps({}))
    os.makedirs("./Temp/IncomingDir", exist_ok=True)
    yield None
    os.remove("./config.json")


def test_should_read_correct_config(setup_full_config_file):
    config = Config()
    assert config.incoming_dir == "./Temp/IncomingDir"
    assert config.library_dir == "./Temp/LibraryDir"
    assert config.library_ignore_dirs == ['./Temp/NoDate', './Temp/Special']
    assert config.working_dir == "./Temp/WorkingDir"
    assert config.md5_size_limit == 666


def test_should_provide_correct_default(setup_minimum_config_file):
    config = Config()
    assert config.incoming_dir == "./Temp/IncomingDir"
    assert config.library_dir == os.getcwd()
    assert config.library_ignore_dirs == []
    assert config.working_dir == os.path.join(os.getcwd(), ".PhotoOrganizer/")
    assert config.md5_size_limit == 512


def test_incoming_dir_missing_should_throw(setup_missing_key_config_file):
    with pytest.raises(InvalidConfigException):
        config = Config()


def test_library_dir_nonexist_should_throw(setup_full_config_file):
    shutil.rmtree("./Temp/LibraryDir", ignore_errors=True)

    with pytest.raises(InvalidConfigException):
        config = Config()


def test_incoming_dir_nonexist_should_throw(setup_full_config_file):
    shutil.rmtree("./Temp/IncomingDir", ignore_errors=True)

    with pytest.raises(InvalidConfigException):
        config = Config()
