class Request:
    __slots__ = ["path", "method", "db", "route", "url_params"]

    def __init__(self, environ, db):
        self.method = environ["REQUEST_METHOD"].upper()
        self.path = get_str_from_wsgi(environ, "PATH_INFO", "/").replace("/", "", 1)
        self.db = db
        self.route = None
        self.url_params = {}


def get_str_from_wsgi(environ, key, default):
    value = environ.get(key, default)
    return value.encode("iso-8859-1").decode()
