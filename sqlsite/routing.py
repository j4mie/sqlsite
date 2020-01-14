from functools import lru_cache
from sqlsite.database import install_function

import re

PATH_MATCH_FUNCTION_NAME = "PATH_MATCH"

PATTERN_COMPONENT_RE = re.compile(r"<(?P<param_type>[a-z]+):(?P<param_name>[a-z_]+)>")

PATTERN_PARAM_TYPES = {
    "str": "[^/]+",
    "int": "[0-9]+",
    "slug": "[-a-zA-Z0-9_]+",
    "uuid": "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    "path": ".+",
}


class MatchedRoute:
    __slots__ = ["pattern", "handler", "config", "existsquery", "url_params"]

    def __init__(self, pattern, handler, config, existsquery, url_params):
        self.pattern = pattern
        self.handler = handler
        self.config = config
        self.existsquery = existsquery
        self.url_params = url_params


@lru_cache(maxsize=64)
def pattern_to_regex(pattern):
    """
    Convert a pattern containing <type:name> syntax to a regex.
    Based on similar code in Django. This is trivially cacheable
    as the same input pattern will always return the same regex.
    """
    parts = ["^"]
    while True:
        match = PATTERN_COMPONENT_RE.search(pattern)
        if not match:
            parts.append(re.escape(pattern))
            break
        parts.append(re.escape(pattern[: match.start()]))
        pattern = pattern[match.end() :]
        param_type, param_name = match.group("param_type", "param_name")
        param_regex = PATTERN_PARAM_TYPES[param_type]
        parts.append(f"(?P<{param_name}>{param_regex})")
    parts.append("$")
    return "".join(parts)


def search_path(pattern, path):
    """
    Given a pattern (ie the contents of the pattern column in the route table) and the
    path of an incoming request (without the leading slash), convert the
    pattern to a regex and return a match object captured from the path
    """
    regex = pattern_to_regex(pattern)
    if regex.endswith("/$"):
        regex = regex[:-2] + "/?$"
    return re.search(regex, path)


def create_path_match_function(path):
    """
    Given the path of an incoming request, create a function that can be used to
    check whether a pattern matches the path.
    """

    def path_match(pattern):
        return search_path(pattern, path) is not None

    return path_match


def install_path_match_function(db, path):
    """
    Install a custom function to match path patterns in the database
    to the path of the incoming request
    """
    install_function(
        db,
        PATH_MATCH_FUNCTION_NAME,
        create_path_match_function(path),
        numargs=1,
        deterministic=True,
    )


def route(db, path):
    install_path_match_function(db, path)
    query = f"SELECT * FROM route WHERE {PATH_MATCH_FUNCTION_NAME}(pattern) LIMIT 1"
    row = db.cursor().execute(query).fetchone()
    if row:
        return MatchedRoute(
            pattern=row["pattern"],
            handler=row["handler"],
            config=row["config"],
            existsquery=row["existsquery"],
            url_params=search_path(row["pattern"], path).groupdict(),
        )
