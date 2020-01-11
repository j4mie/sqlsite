from . import sqlar
from .responses import JSONResponse, NotFoundResponse, Response, StreamingResponse
from mimetypes import guess_type

import os


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


def static(request):
    path = os.path.join(request.route.config, request.route.url_params["name"])
    file_row = sqlar.get_row(request.db, path)
    if not file_row:
        return NotFoundResponse()

    blob = sqlar.get_blob(request.db, file_row)
    media_type = guess_type(path)[0] or "text/plain"
    is_compressed = blob.length() != file_row["sz"]
    headers = [("Content-Encoding", "deflate")] if is_compressed else []

    def chunks():
        while True:
            chunk = blob.read(8192)
            if not chunk:
                break
            yield chunk

    return StreamingResponse(headers, chunks(), media_type, str(blob.length()))


def get_handler(name):
    return {"hello": hello, "json": json, "static": static}[name]
