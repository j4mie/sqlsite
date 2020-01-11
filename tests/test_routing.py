from .utils import create_route
from sqlsite.database import connect
from sqlsite.routing import (
    create_path_match_function,
    install_path_match_function,
    PATH_MATCH_FUNCTION_NAME,
    route,
)


def test_route(db):
    create_route(db, "somepath/", "testhandler")
    path = "somepath/"
    result = route(db, path)
    assert result.handler == "testhandler"


def test_route_match(db):
    create_route(db, "somepath/", "testhandler")
    path = "someotherpath/"
    result = route(db, path)
    assert result is None


def test_path_match_function():
    path_match_function = create_path_match_function("path/")
    assert path_match_function("path/")
    assert path_match_function("path")
    assert not path_match_function("otherpath/")


def test_install_path_match_function():
    db = connect(":memory:")
    install_path_match_function(db, "path/")
    sql = f"SELECT {PATH_MATCH_FUNCTION_NAME}('path/')"
    assert db.cursor().execute(sql).fetchone()[0]
