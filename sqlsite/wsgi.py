from .database import connect
from .exists import check_exists_query
from .handlers import get_handler
from .request import Request
from .responses import NotFoundResponse, PermanentRedirectResponse
from .routing import route, search_path


def should_append_slash(request):
    return request.route.pattern.endswith("/$") and not request.path.endswith("/")


def get_response(request):
    matched_route = route(request.db, request.path)
    if not matched_route:
        return NotFoundResponse()
    request.route = matched_route
    if should_append_slash(request):
        return PermanentRedirectResponse(f"/{request.path}/")
    if not check_exists_query(request):
        return NotFoundResponse()
    handler = get_handler(matched_route.handler)
    response = handler(request)
    return response


def make_app(test_db=None):
    def app(environ, start_response):
        db = test_db or connect("db.sqlite")
        request = Request(environ, db)
        response = get_response(request)
        start_response(response.get_status_line(), response.get_headers())
        return response.get_content()

    return app