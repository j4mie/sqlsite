from sqlsite.database import (
    connect,
    create_path_match_function,
    install_path_match_function,
    install_row_factory,
    row_factory,
)


class MockCursor:
    def getdescription(self):
        return [("col1",), ("col2",)]


def test_connect():
    db = connect(":memory:")
    sql = "SELECT 1"
    result = db.cursor().execute(sql).fetchone()
    assert result[0] == 1


def test_row_factory():
    cursor = MockCursor()
    row = ("a", "b")
    result = row_factory(cursor, row)
    assert result[0] == "a"
    assert result[1] == "b"
    assert result["col1"] == "a"
    assert result["col2"] == "b"


def test_install_row_factory():
    db = connect(":memory:")
    install_row_factory(db)
    sql = "WITH t(col1, col2) AS (VALUES ('a', 'b')) SELECT * FROM t"
    result = db.cursor().execute(sql).fetchone()
    assert result[0] == "a"
    assert result[1] == "b"
    assert result["col1"] == "a"
    assert result["col2"] == "b"


def test_path_match_function():
    path_match_function = create_path_match_function("path/")
    assert path_match_function("path/")
    assert path_match_function("path")
    assert not path_match_function("otherpath/")


def test_install_path_match_function():
    db = connect(":memory:")
    install_path_match_function(db, "path/")
    assert db.cursor().execute("SELECT PATH_MATCH('path/')").fetchone()[0]
    assert db.cursor().execute("SELECT PATH_MATCH('path')").fetchone()[0]
    assert not db.cursor().execute("SELECT PATH_MATCH('otherpath/')").fetchone()[0]
