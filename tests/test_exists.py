from .utils import create_route
from sqlsite.exists import run_existsquery
from sqlsite.wsgi import make_app

import httpx


def test_existsquery_returns_true(db):
    assert run_existsquery(db, "SELECT 1", {})


def test_existsquery_returns_false(db):
    assert not run_existsquery(db, "SELECT 0", {})


def test_missing_existsquery_returns_true(db):
    assert run_existsquery(db, "", {})


def test_existsquery_request(db):
    create_route(db, "", "hello", existsquery="SELECT 0")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/")
    assert response.status_code == 404
