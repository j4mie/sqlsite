from ..utils import create_route
from sqlsite.wsgi import make_app

import httpx


def test_json_handler(db):
    sql = "WITH t(greeting) AS (VALUES('hello')) SELECT * FROM t"
    create_route(db, "^$", "json", config=sql)
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/")
    assert response.status_code == 200
    assert response.json() == [{"greeting": "hello"}]
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Content-Length"] == "23"
