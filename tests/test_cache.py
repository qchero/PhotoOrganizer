import os
from pathlib import Path
from unittest.mock import Mock

import pytest

from photo_organizer.cache import Cache


@pytest.fixture
def cache():
    config = Mock()
    config.working_dir = Path("./Temp/")
    cache = Cache(config)
    yield cache
    cache._conn.close()


def fill_cache(cache):
    cache.upsert_hashcode_doc(Path("./1.JPG"), "123", 1024)
    cache.upsert_hashcode_doc(Path("./2.JPG"), "456", 1024)
    cache.upsert_hashcode_doc(Path("./3.JPG"), "789", 1024)


class Test_upsert_hashcode_doc:
    def test_create_db_file(self, cache):
        cache.upsert_hashcode_doc(Path("./1.jpg"), "123", 1024)

        assert os.path.exists("./Temp/database.db")

    def test_override_doc(self, cache):
        cache.upsert_hashcode_doc(Path("./1.jpg"), "321", 1024)

        doc = cache.get_doc_by_path(Path("./1.jpg"))
        assert doc.hashcode == "321"


class Test_get_all:
    def test_return_all(self, cache):
        fill_cache(cache)
        docs = cache.get_all()
        assert len(docs) == 3
        assert set([doc.path for doc in docs]) == {Path("./1.jpg"), Path("./2.jpg"), Path("./3.jpg")}
        assert set([doc.hashcode for doc in docs]) == {"123", "456", "789"}
        assert set([doc.size for doc in docs]) == {1024}


class Test_get_doc_by_path:
    def test_should_return_correct_result(self, cache):
        fill_cache(cache)
        assert cache.get_doc_by_path(Path("./0.jpg")) is None
        assert cache.get_doc_by_path(Path("./1.jpg")).hashcode == "123"


class Test_get_docs_by_hashcode:
    def test_should_return_correct_result(self, cache):
        fill_cache(cache)
        cache.upsert_hashcode_doc(Path("./2_copy.jpg"), "456", 1024)

        assert cache.get_docs_by_hashcode("666") == []
        assert cache.get_docs_by_hashcode("123")[0].path == Path("./1.jpg")
        assert len(cache.get_docs_by_hashcode("456")) == 2


class Test_delete_by_path:
    def test_should_delete(self, cache):
        fill_cache(cache)
        cache.delete_by_path(Path("./2.jpg"))
        assert len(cache.get_all()) == 2
        assert cache.get_doc_by_path(Path("./2.jpg")) is None
