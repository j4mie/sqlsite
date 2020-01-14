from .sql import maybe_get_sql_from_file


def run_existsquery(db, query_or_prefixed_filename, params):
    if not query_or_prefixed_filename:
        return True
    query = maybe_get_sql_from_file(db, query_or_prefixed_filename)
    return db.cursor().execute(query, params).fetchone()[0]


def check_existsquery(request):
    return run_existsquery(
        request.db, request.route.existsquery, request.route.url_params
    )
