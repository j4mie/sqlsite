from . import sqlar

PREFIX = "file="


def maybe_get_sql_from_file(db, sql_or_prefixed_filename):
    if sql_or_prefixed_filename.startswith(PREFIX):
        filename = sql_or_prefixed_filename[len(PREFIX) :]
        row = sqlar.get_row(db, filename)
        return sqlar.get_data(db, row).decode("utf-8")
    return sql_or_prefixed_filename
