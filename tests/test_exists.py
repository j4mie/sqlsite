from .utils import create_route
from sqlsite.exists import run_exists_query
from sqlsite.wsgi import make_app

import httpx


def test_exists_query_returns_true(db):
    assert run_exists_query(db, "SELECT 1", {})


def test_exists_query_returns_false(db):
    assert not run_exists_query(db, "SELECT 0", {})


def test_missing_exists_query_returns_true(db):
    assert run_exists_query(db, "", {})


def test_exists_query_request(db):
    create_route(db, "^$", "hello", exists_query="SELECT 0")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/")
    assert response.status_code == 404
