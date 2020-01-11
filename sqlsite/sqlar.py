from zlib import decompress


def get_row(db, name):
    query = "SELECT rowid, sz FROM sqlar WHERE name=:name"
    return db.cursor().execute(query, {"name": name}).fetchone()


def get_blob(db, row):
    return db.blobopen("main", "sqlar", "data", row["rowid"], False)


def get_data(db, row):
    blob = get_blob(db, row)
    length = blob.length()
    data = blob.read()
    return decompress(data) if row["sz"] != length else data
