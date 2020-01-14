from zlib import compress


def create_route_table(db):
    sql = """
    CREATE TABLE route (
        pattern TEXT PRIMARY KEY NOT NULL,
        handler TEXT NOT NULL,
        config TEXT NOT NULL,
        existsquery TEXT
    );
    """
    db.cursor().execute(sql)


def create_route(db, pattern, handler, config="", existsquery=None):
    sql = "INSERT INTO route VALUES (:pattern, :handler, :config, :existsquery)"
    params = {
        "pattern": pattern,
        "handler": handler,
        "config": config,
        "existsquery": existsquery,
    }
    db.cursor().execute(sql, params)


def ensure_sqlar_table(db):
    sql = """
    CREATE TABLE IF NOT EXISTS sqlar(
        name TEXT PRIMARY KEY,  -- name of the file
        mode INT,               -- access permissions
        mtime INT,              -- last modification time
        sz INT,                 -- original file size
        data BLOB               -- compressed content
        );
    """
    db.cursor().execute(sql)


def create_sqlar_file(db, name, data):
    ensure_sqlar_table(db)
    compressed = compress(data)
    maybe_compressed_data = compressed if len(compressed) < len(data) else data
    sql = "INSERT INTO sqlar VALUES (:name, 33188, time('now'), :sz, :data)"
    params = {"name": name, "data": maybe_compressed_data, "sz": len(data)}
    db.cursor().execute(sql, params)
