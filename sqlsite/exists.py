def run_exists_query(db, query, params):
    if not query:
        return True
    return db.cursor().execute(query, params).fetchone()[0]


def check_exists_query(request):
    query = request.route["exists_query"]
    params = request.url_params
    return run_exists_query(request.db, query, params)
