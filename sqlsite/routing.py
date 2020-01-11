from sqlsite.database import install_function

import re

PATH_MATCH_FUNCTION_NAME = "PATH_MATCH"


class MatchedRoute:
    __slots__ = ["pattern", "handler", "config", "exists_query", "url_params"]

    def __init__(self, pattern, handler, config, exists_query, url_params):
        self.pattern = pattern
        self.handler = handler
        self.config = config
        self.exists_query = exists_query
        self.url_params = url_params


def search_path(pattern, path):
    if pattern.endswith("/$"):
        pattern = pattern[:-2] + "/?$"
    return re.search(pattern, path)


def create_path_match_function(path):
    def path_match(val):
        return search_path(val, path) is not None

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
            exists_query=row["exists_query"],
            url_params=search_path(row["pattern"], path).groupdict(),
        )
