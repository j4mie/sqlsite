from .utils import create_route, create_sqlar_file
from sqlsite.exists import run_existsquery
from sqlsite.wsgi import make_app

import httpx


def test_existsquery_returns_true(db):
    assert run_existsquery(db, "SELECT 1", {})


def test_existsquery_returns_false(db):
    assert not run_existsquery(db, "SELECT 0", {})


def test_missing_existsquery_returns_true(db):
    assert run_existsquery(db, "", {})


def test_existsquery_in_file(db):
    query = "SELECT 0"
    create_sqlar_file(db, "query.sql", query.encode())
    assert not run_existsquery(db, "file=query.sql", {})


def test_existsquery_request(db):
    create_route(db, "", "hello", existsquery="SELECT 0")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/")
    assert response.status_code == 404
