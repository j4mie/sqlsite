from .fixtures import in_memory_db as db
from .utils import create_route
from sqlsite.wsgi import make_app

import httpx


def test_hello_world(db):
    create_route(db, "^$", "hello")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/")
    assert response.status_code == 200
    assert response.text == "Hello from SQLSite"
    assert response.headers["Content-Type"] == "text/plain"
    assert response.headers["Content-Length"] == "18"


def test_not_found(db):
    create_route(db, "^$", "hello")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/notfound")
    assert response.status_code == 404
    assert response.text == "Not Found"
    assert response.headers["Content-Type"] == "text/plain"
