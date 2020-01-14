from . import sqlar
from .responses import (
    HTMLResponse,
    JSONResponse,
    NotFoundResponse,
    PermanentRedirectResponse,
    Response,
    StreamingResponse,
)
from .sql import maybe_get_sql_from_file
from mimetypes import guess_type

import jinja2
import os

try:
    import misaka
except ImportError:
    misaka = None


def hello(request):
    return Response(content="Hello from SQLSite")


def json(request):
    sql = maybe_get_sql_from_file(request.db, request.route.config)
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
    is_compressed = file_row["sz"] != blob.length()
    headers = [("Content-Encoding", "deflate")] if is_compressed else []

    def chunks():
        while True:
            chunk = blob.read(8192)
            if not chunk:
                break
            yield chunk

    return StreamingResponse(headers, chunks(), media_type, str(blob.length()))


class SQLArchiveTemplateLoader(jinja2.BaseLoader):
    def __init__(self, db):
        self.db = db

    def get_source(self, environment, template):
        file_row = sqlar.get_row(self.db, template)
        if not file_row:
            raise jinja2.TemplateNotFound(template)
        source = sqlar.get_data(self.db, file_row).decode("utf-8")
        return source, template, lambda: False


def markdown_filter(*args, **kwargs):
    return jinja2.Markup(misaka.html(*args, **kwargs))


def template(request):
    jinja2_env = jinja2.Environment(
        loader=SQLArchiveTemplateLoader(request.db), autoescape=True,
    )
    if misaka:
        jinja2_env.filters["markdown"] = markdown_filter
    template = jinja2_env.get_template(request.route.config)

    def sql(sql_or_prefixed_filename, params=None):
        sql = maybe_get_sql_from_file(request.db, sql_or_prefixed_filename)
        params = params or {}
        return request.db.cursor().execute(sql, params).fetchall()

    context = {
        "sql": sql,
        "url": request.route.url_params,
    }
    content = template.render(context)
    return HTMLResponse(content=content)


def redirect(request):
    sql = maybe_get_sql_from_file(request.db, request.route.config)
    params = request.route.url_params
    location = request.db.cursor().execute(sql, params).fetchone()[0]
    return PermanentRedirectResponse(location)


def get_handler(name):
    return {
        "hello": hello,
        "json": json,
        "redirect": redirect,
        "static": static,
        "template": template,
    }[name]
