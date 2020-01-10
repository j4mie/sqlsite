from .fixtures import in_memory_db as db
from .utils import create_route
from sqlsite.routing import route


def test_route(db):
    create_route(db, "somepath/", "testhandler")
    path = "somepath/"
    result = route(db, path)
    assert result["handler"] == "testhandler"


def test_route_match(db):
    create_route(db, "somepath/", "testhandler")
    path = "someotherpath/"
    result = route(db, path)
    assert result is None
