from urllib.parse import parse_qs


class Request:
    __slots__ = ["path", "method", "query", "db", "route"]

    def __init__(self, environ, db):
        self.method = environ["REQUEST_METHOD"].upper()
        self.path = get_str_from_wsgi(environ, "PATH_INFO", "/").replace("/", "", 1)
        self.query = parse_qs(get_str_from_wsgi(environ, "QUERY_STRING", ""))
        self.db = db
        self.route = None


def get_str_from_wsgi(environ, key, default):
    value = environ.get(key, default)
    return value.encode("iso-8859-1").decode()
