from ..utils import create_route
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
