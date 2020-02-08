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
