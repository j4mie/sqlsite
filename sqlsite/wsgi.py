from .database import connect
from .handlers import get_handler
from .request import Request
from .routing import route


def make_app(test_db=None):
    def app(environ, start_response):
        db = test_db or connect("db.sqlite")
        request = Request(environ, db)
        matched_route = route(db, request.path)
        handler = get_handler(matched_route["handler"])
        response = handler(request)
        start_response(response.get_status_line(), response.get_headers())
        return response.get_content()

    return app
