import apsw
import re


def connect(name):
    return apsw.Connection(name)


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


def create_path_match_function(path):
    def path_match(val):
        if val.endswith("/$"):
            val = val[:-2] + "/?$"
        return re.search(val, path) is not None

    return path_match


def install_path_match_function(db, path):
    """
    Install a custom function to match path patterns in the database
    to the path of the incoming request
    """
    path_match_function = create_path_match_function(path)
    db.createscalarfunction("PATH_MATCH", path_match_function, 1)
