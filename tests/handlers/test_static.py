from ..utils import create_route, create_sqlar_file
from sqlsite.wsgi import make_app

import httpx
import pytest


@pytest.mark.skip("Something weird is going on with httpx")
def test_static_handler(db):
    create_route(db, "<path:name>", "static", config="")
    create_sqlar_file(db, "hello.txt", b"hello")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/hello.txt")
    assert response.status_code == 200
    assert response.content == b"hello"
    assert response.headers["Content-Type"] == "text/plain"
    assert response.headers["Content-Length"] == "5"
