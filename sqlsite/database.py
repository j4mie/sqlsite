import apsw
import os


def get_readonly_connection(name):
    return apsw.Connection(name, flags=apsw.SQLITE_OPEN_READONLY)


def connect(name=None):
    name = name or os.environ.get("SQLSITE_DATABASE", "db.sqlite")
    db = get_readonly_connection(name)
    install_row_factory(db)
    return db


def row_factory(cursor, row):
    columns = [column[0] for column in cursor.getdescription()]
    result = {}
    for index, value in enumerate(row):
        result[columns[index]] = value
        result[index] = value
    return result


def install_row_factory(db):
    """
    Install a function that return rows that are indexable by string key or int index
    # TODO - make this better!
    """
    db.setrowtrace(row_factory)


def install_function(db, name, callable, numargs=1, deterministic=False):
    db.createscalarfunction(name, callable, numargs, deterministic)
