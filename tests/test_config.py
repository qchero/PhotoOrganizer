import json
import os
import shutil
from pathlib import Path

import pytest

from exception.exception import InvalidConfigException
from photo_organizer.config import Config


@pytest.fixture()
def setup_full_config_file():
    full_config = {
        "IncomingDir": "Temp/IncomingDir"
    }
    with open("./config.json", "w") as config_file:
        config_file.write(json.dumps(full_config))
    os.makedirs("./Temp/IncomingDir", exist_ok=True)
    yield None
    os.remove("./config.json")


@pytest.fixture()
def setup_minimum_config_file():
    with open("./config.json", "w") as config_file:
        config_file.write(json.dumps({
            "IncomingDir": "Temp/IncomingDir"
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
    assert config.cur_working_dir == Path(".")
    assert config.incoming_dir == Path("Temp/IncomingDir")
    assert config.working_dir == Path(".PhotoOrganizer")
    assert config.md5_size_limit == 100


def test_should_provide_correct_default(setup_minimum_config_file):
    config = Config()
    assert config.cur_working_dir == Path(".")
    assert config.incoming_dir == Path("Temp/IncomingDir")
    assert config.working_dir == Path(".PhotoOrganizer")
    assert config.md5_size_limit == 100


def test_config_file_missing_should_throw():
    with pytest.raises(InvalidConfigException):
        Config()


def test_incoming_dir_missing_should_throw(setup_missing_key_config_file):
    with pytest.raises(InvalidConfigException):
        Config()


def test_incoming_dir_nonexist_should_throw(setup_full_config_file):
    shutil.rmtree("./Temp/IncomingDir", ignore_errors=True)

    with pytest.raises(InvalidConfigException):
        Config()
