import os
import shutil
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def conf_each_function():
    """
    Fixture to create a Temp folder as CWD for testing, and clean up when tests are done
    @return:
    """
    temp_path = Path("./Temp/")
    shutil.rmtree(temp_path, ignore_errors=True)
    temp_path.mkdir(exist_ok=True)
    os.chdir(temp_path)
    yield None
    os.chdir("..")
    shutil.rmtree(temp_path, ignore_errors=True)
