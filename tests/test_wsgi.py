from .utils import create_route
from sqlsite.wsgi import make_app

import httpx


def test_hello_world(db):
    create_route(db, "", "hello")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/")
    assert response.status_code == 200
    assert response.text == "Hello from SQLSite"
    assert response.headers["Content-Type"] == "text/plain"
    assert response.headers["Content-Length"] == "18"


def test_not_found(db):
    create_route(db, "", "hello")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/notfound")
    assert response.status_code == 404
    assert response.text == "Not Found"
    assert response.headers["Content-Type"] == "text/plain"


def test_add_trailing_slash(db):
    create_route(db, "hello/", "hello")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/hello", allow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"] == "/hello/"


def test_post_put_patch_ignored(db):
    app = make_app(db)
    client = httpx.Client(app=app)
    for method in ["POST", "PUT", "PATCH"]:
        response = client.request(method, "http://test/")
        assert response.status_code == 405
