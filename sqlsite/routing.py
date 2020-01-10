from sqlsite.database import install_path_match_function


def route(db, path):
    install_path_match_function(db, path)
    query = "SELECT * FROM route WHERE PATH_MATCH(pattern) LIMIT 1"
    return db.cursor().execute(query).fetchone()
