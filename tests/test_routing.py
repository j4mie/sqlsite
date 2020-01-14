from .utils import create_route
from sqlsite.database import connect
from sqlsite.routing import (
    create_path_match_function,
    install_path_match_function,
    PATH_MATCH_FUNCTION_NAME,
    pattern_to_regex,
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
    assert not path_match_function("otherpath/")


def test_path_match_function_with_params():
    path_match_function = create_path_match_function("path/test/")
    assert path_match_function("path/<str:param>/")
    assert not path_match_function("path/<int:param/")


def test_trailing_slash_behaviour():
    path_match_function = create_path_match_function("path")
    assert path_match_function("path")
    assert path_match_function("path/")


def test_install_path_match_function():
    db = connect(":memory:")
    install_path_match_function(db, "path/")
    sql = f"SELECT {PATH_MATCH_FUNCTION_NAME}('path/')"
    assert db.cursor().execute(sql).fetchone()[0]


def test_string_component():
    pattern = "test/<str:param>/"
    regex = pattern_to_regex(pattern)
    assert regex == "^test/(?P<param>[^/]+)/$"


def test_int_component():
    pattern = "test/<int:param>/"
    regex = pattern_to_regex(pattern)
    assert regex == "^test/(?P<param>[0-9]+)/$"


def test_slug_component():
    pattern = "test/<slug:param>/"
    regex = pattern_to_regex(pattern)
    assert regex == "^test/(?P<param>[-a-zA-Z0-9_]+)/$"


def test_uuid_component():
    pattern = "test/<uuid:param>/"
    regex = pattern_to_regex(pattern)
    assert regex == (
        "^test/"
        "(?P<param>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$"
    )


def test_path_component():
    pattern = "test/<path:param>"
    regex = pattern_to_regex(pattern)
    assert regex == "^test/(?P<param>.+)$"


def test_multiple_components():
    pattern = "test/<int:first>/<slug:second>/something/<str:third>/"
    regex = pattern_to_regex(pattern)
    assert regex == (
        "^test/(?P<first>[0-9]+)"
        "/(?P<second>[-a-zA-Z0-9_]+)"
        "/something/(?P<third>[^/]+)/$"
    )
