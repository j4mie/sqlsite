from .responses import JSONResponse, Response


def hello(request):
    return Response(content="Hello from SQLSite")


def json(request):
    sql = request.route.config
    params = request.route.url_params
    results = request.db.cursor().execute(sql, params).fetchall()
    results_with_string_keys_only = [
        {key: result[key] for key in result.keys() if isinstance(key, str)}
        for result in results
    ]
    return JSONResponse(results_with_string_keys_only)


def get_handler(name):
    return {"hello": hello, "json": json}[name]
