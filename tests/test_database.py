from sqlsite.database import connect, get_readonly_connection, row_factory

import apsw


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


def test_row_factory_installed():
    db = connect(":memory:")
    sql = "WITH t(col1, col2) AS (VALUES ('a', 'b')) SELECT * FROM t"
    result = db.cursor().execute(sql).fetchone()
    assert result[0] == "a"
    assert result[1] == "b"
    assert result["col1"] == "a"
    assert result["col2"] == "b"


def test_database_name_default(mocker):
    mock = mocker.patch("sqlsite.database.get_readonly_connection")
    connect()
    mock.assert_called_with("db.sqlite")


def test_database_name_env_var(mocker):
    mocker.patch.dict("os.environ", {"SQLSITE_DATABASE": "somedb.sqlite"})
    mock = mocker.patch("sqlsite.database.get_readonly_connection")
    connect()
    mock.assert_called_with("somedb.sqlite")


def test_database_opened_readonly(mocker):
    db = get_readonly_connection(":memory:")
    assert db.open_flags == apsw.SQLITE_OPEN_READONLY
