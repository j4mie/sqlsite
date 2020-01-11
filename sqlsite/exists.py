def run_exists_query(db, query, params):
    if not query:
        return True
    return db.cursor().execute(query, params).fetchone()[0]


def check_exists_query(request):
    return run_exists_query(
        request.db, request.route.exists_query, request.route.url_params
    )
