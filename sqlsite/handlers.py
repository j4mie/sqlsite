from .responses import Response
from http import HTTPStatus


def hello(request):
    return Response(content="Hello from SQLSite")


def get_handler(name):
    return {"hello": hello,}[name]
