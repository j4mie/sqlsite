from ..utils import create_route, create_sqlar_file
from sqlsite.wsgi import make_app

import httpx


def test_redirect_handler(db):
    sql = "SELECT '/after/' || :slug || '/'"
    create_route(db, "before/<slug:slug>/", "redirect", config=sql)
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/before/hello/", allow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"] == "/after/hello/"


def test_redirect_with_sql_in_file(db):
    sql = "SELECT '/after/' || :slug || '/'"
    create_sqlar_file(db, "query.sql", sql.encode())
    create_route(db, "before/<slug:slug>/", "redirect", config="file=query.sql")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/before/hello/", allow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"] == "/after/hello/"
