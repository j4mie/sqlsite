import apsw
import os


class Row(dict):
    """
    A dictionary with one extra feature: it supports lookup of values
    by index. This implementation works because dictionaries in Python
    3.7+ are guaranteed to return their values in insertion order.
    """

    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self.values())[key]
        return super().__getitem__(key)


def get_readonly_connection(name):
    return apsw.Connection(name, flags=apsw.SQLITE_OPEN_READONLY)


def connect(name=None):
    name = name or os.environ.get("SQLSITE_DATABASE", "db.sqlite")
    db = get_readonly_connection(name)
    install_row_factory(db)
    return db


def row_factory(cursor, row):
    columns = [column[0] for column in cursor.getdescription()]
    return Row(zip(columns, row))


def install_row_factory(db):
    """
    Install a function that return rows that are indexable by string key or int index
    # TODO - make this better!
    """
    db.setrowtrace(row_factory)


def install_function(db, name, callable, numargs=1, deterministic=False):
    db.createscalarfunction(name, callable, numargs, deterministic)
