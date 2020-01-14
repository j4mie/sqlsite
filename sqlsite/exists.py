def run_existsquery(db, query, params):
    if not query:
        return True
    return db.cursor().execute(query, params).fetchone()[0]


def check_existsquery(request):
    return run_existsquery(
        request.db, request.route.existsquery, request.route.url_params
    )
