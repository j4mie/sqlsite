from .database import connect
from .exists import check_existsquery
from .handlers import get_handler
from .request import Request
from .responses import (
    ErrorResponse,
    MethodNotAllowedResponse,
    NotFoundResponse,
    PermanentRedirectResponse,
)
from .routing import route

import logging

logger = logging.getLogger("sqlsite")


def should_append_slash(request):
    return request.route.pattern.endswith("/") and not request.path.endswith("/")


def method_allowed(request):
    return request.method in {"GET", "HEAD"}


def get_response(request):
    if not method_allowed(request):
        return MethodNotAllowedResponse()
    matched_route = route(request.db, request.path)
    if not matched_route:
        return NotFoundResponse()
    request.route = matched_route
    if should_append_slash(request):
        return PermanentRedirectResponse(f"/{request.path}/")
    if not check_existsquery(request):
        return NotFoundResponse()
    handler = get_handler(matched_route.handler)
    response = handler(request)
    return response


def make_app(test_db=None):
    def app(environ, start_response):
        db = test_db or connect()
        request = Request(environ, db)
        try:
            response = get_response(request)
        except Exception as exception:
            logger.exception(exception)
            response = ErrorResponse()
        start_response(response.get_status_line(), response.get_headers())
        return response.get_content()

    return app
