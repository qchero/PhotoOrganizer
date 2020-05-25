import os
import shutil
from unittest.mock import Mock

import pytest

from photo_organizer.cache import Cache


@pytest.fixture(autouse=True)
def each_function():
    temp_path = "./Temp/"
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path, ignore_errors=True)
    os.makedirs(temp_path, exist_ok=True)
    yield None
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path, ignore_errors=True)
    if os.path.exists("./.PhotoOrganizer"):
        shutil.rmtree("./.PhotoOrganizer", ignore_errors=True)


@pytest.fixture
def cache():
    config = Mock()
    config.working_dir = "./Temp/"
    config.library_dir = "./"
    cache = Cache(config)
    yield cache
    cache._conn.close()


def fill_cache(cache):
    cache.upsert_hashcode_doc("./1.jpg", "123", 1024)
    cache.upsert_hashcode_doc("./2.jpg", "456", 1024)
    cache.upsert_hashcode_doc("./3.jpg", "789", 1024)


class TestUpsertHashcodeDoc:
    def test_create_db_file(self, cache):
        cache.upsert_hashcode_doc("./1.jpg", "123", 1024)

        assert os.path.exists("./Temp/database.db")

    def test_override_doc(self, cache):
        cache.upsert_hashcode_doc("./1.jpg", "321", 1024)

        doc = cache.get_doc_by_path("./1.jpg")
        assert doc.hashcode == "321"


class TestGetAll:
    def test_return_all(self, cache):
        fill_cache(cache)
        docs = cache.get_all()
        assert len(docs) == 3
        assert set([doc.path for doc in docs]) == {"1.jpg", "2.jpg", "3.jpg"}
        assert set([doc.hashcode for doc in docs]) == {"123", "456", "789"}
        assert set([doc.size for doc in docs]) == {1024}


class TestGetByPath:
    def test_should_return_correct_result(self, cache):
        fill_cache(cache)
        assert cache.get_doc_by_path("./0.jpg") is None
        assert cache.get_doc_by_path("./1.jpg").hashcode == "123"


class TestGetByHash:
    def test_should_return_correct_result(self, cache):
        fill_cache(cache)
        cache.upsert_hashcode_doc("./2_copy.jpg", "456", 1024)

        assert cache.get_docs_by_hashcode("666") == []
        assert cache.get_docs_by_hashcode("123")[0].path == "1.jpg"
        assert len(cache.get_docs_by_hashcode("456")) == 2


class TestDeleteByPath:
    def test_should_delete(self, cache):
        fill_cache(cache)
        cache.delete_by_path("./2.jpg")
        assert len(cache.get_all()) == 2
        assert cache.get_doc_by_path("./2.jpg") is None
