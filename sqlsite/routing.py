from sqlsite.database import install_function

import re

PATH_MATCH_FUNCTION_NAME = "PATH_MATCH"


def search_path(pattern, path):
    return re.search(pattern, path)


def create_path_match_function(path):
    def path_match(val):
        if val.endswith("/$"):
            val = val[:-2] + "/?$"
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
    return db.cursor().execute(query).fetchone()
