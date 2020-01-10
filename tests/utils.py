from sqlsite.database import connect, install_row_factory


def create_route_table(db):
    sql = """
    CREATE TABLE route (
        pattern TEXT PRIMARY KEY NOT NULL,
        handler TEXT NOT NULL,
        config TEXT NOT NULL,
        exists_query TEXT
    );
    """
    db.cursor().execute(sql)


def create_route(db, pattern, handler, config="", exists_query=None):
    sql = "INSERT INTO route VALUES (:pattern, :handler, :config, :exists_query)"
    params = {
        "pattern": pattern,
        "handler": handler,
        "config": config,
        "exists_query": exists_query,
    }
    db.cursor().execute(sql, params)
