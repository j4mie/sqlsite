from .utils import create_sqlar_file
from sqlsite.sql import maybe_get_sql_from_file


def test_raw_query(db):
    query = "SELECT VALUES('hi')"
    assert maybe_get_sql_from_file(db, query) == query


def test_query_from_file(db):
    query = "SELECT VALUES('hi')"
    create_sqlar_file(db, "query.sql", query.encode())
    assert maybe_get_sql_from_file(db, "file=query.sql") == query
