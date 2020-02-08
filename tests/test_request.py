from sqlsite.request import Request


def test_basic_request(db):
    environ = {
        "REQUEST_METHOD": "get",
        "PATH_INFO": "/test/",
    }
    request = Request(environ, db)
    assert request.method == "GET"
    assert request.path == "test/"
    assert request.db is db
    assert request.route is None


def test_query_string(db):
    environ = {
        "REQUEST_METHOD": "get",
        "PATH_INFO": "/test/",
        "QUERY_STRING": "key1=value1&key2=value2",
    }
    request = Request(environ, db)
    assert request.query == {
        "key1": ["value1"],
        "key2": ["value2"],
    }
