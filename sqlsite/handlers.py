from .responses import Response


def hello(request):
    return Response(content="Hello from SQLSite")


def get_handler(name):
    return {"hello": hello,}[name]
