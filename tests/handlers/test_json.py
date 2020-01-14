from ..utils import create_route, create_sqlar_file
from sqlsite.wsgi import make_app

import httpx


def test_json_handler(db):
    sql = "WITH t(greeting) AS (VALUES('hello')) SELECT * FROM t"
    create_route(db, "", "json", config=sql)
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/")
    assert response.status_code == 200
    assert response.json() == [{"greeting": "hello"}]
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Content-Length"] == "23"


def test_json_handler_with_query_in_file(db):
    sql = "WITH t(greeting) AS (VALUES('hello')) SELECT * FROM t"
    create_sqlar_file(db, "query.sql", sql.encode())
    create_route(db, "", "json", config="file=query.sql")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/")
    assert response.status_code == 200
    assert response.json() == [{"greeting": "hello"}]
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Content-Length"] == "23"
