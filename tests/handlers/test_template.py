from ..utils import create_route, create_sqlar_file
from sqlsite.wsgi import make_app

import httpx


def test_template_handler(db):
    create_route(db, "^(?P<name>[a-z]+)/$", "template", config="template.html")
    create_sqlar_file(db, "template.html", b"<h1>hello {{ url.name }}</h1>")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/world/")
    assert response.status_code == 200
    assert response.text == "<h1>hello world</h1>"
    assert response.headers["Content-Type"] == "text/html"
    assert response.headers["Content-Length"] == "20"


def test_template_with_query(db):
    create_route(db, "^$", "template", config="template.html")
    template = "".join(
        [
            "{% with name = sql(\"VALUES('sql')\")[0][0] %}",
            "<h1>hello {{ name }}</h1>",
            "{% endwith %}",
        ]
    ).encode()
    create_sqlar_file(db, "template.html", template)
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/")
    assert response.status_code == 200
    assert response.text == "<h1>hello sql</h1>"
    assert response.headers["Content-Type"] == "text/html"
    assert response.headers["Content-Length"] == "18"


def test_missing_template(db):
    create_route(db, "^$", "template", config="missingtemplate.html")
    create_sqlar_file(db, "template.html", b"<h1>hello</h1>")
    app = make_app(db)
    client = httpx.Client(app=app)
    response = client.get("http://test/")
    assert response.status_code == 500
