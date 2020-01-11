from sqlsite.database import connect, row_factory


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