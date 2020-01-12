from http import HTTPStatus

import json


class Response:
    def __init__(
        self, status=HTTPStatus.OK, headers=[], content="", content_type="text/plain"
    ):
        self.status = status
        self.headers = headers
        self.content = content
        self.content_type = content_type

    def get_status_line(self):
        return f"{self.status.value} {self.status.phrase}"

    def get_headers(self):
        headers = (
            [self.get_content_length_header()]
            + [self.get_content_type_header()]
            + self.headers
        )
        return [header for header in headers if header]

    def get_content(self):
        return [self.content.encode("utf-8")]

    def get_content_length_header(self):
        return ("Content-Length", str(len(self.content)))

    def get_content_type_header(self):
        return ("Content-Type", self.content_type)


class ErrorResponse(Response):
    def __init__(self):
        super().__init__(
            status=HTTPStatus.INTERNAL_SERVER_ERROR, content="Server Error"
        )


class NotFoundResponse(Response):
    def __init__(self):
        super().__init__(status=HTTPStatus.NOT_FOUND, content="Not Found")


class PermanentRedirectResponse(Response):
    def __init__(self, redirect_to):
        super().__init__(
            status=HTTPStatus.MOVED_PERMANENTLY, headers=[("Location", redirect_to)]
        )


class MethodNotAllowedResponse(Response):
    def __init__(self):
        super().__init__(
            status=HTTPStatus.METHOD_NOT_ALLOWED, content="Method not allowed"
        )


class JSONResponse(Response):
    def __init__(self, data):
        super().__init__(content=json.dumps(data), content_type="application/json")


class HTMLResponse(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(content_type="text/html", *args, **kwargs)


class StreamingResponse(Response):
    def __init__(self, headers, content_iterable, content_type, content_length=None):
        self.status = HTTPStatus.OK
        self.headers = headers
        self.content_iterable = content_iterable
        self.content_type = content_type
        self.content_length = content_length

    def get_content(self):
        return self.content_iterable

    def get_content_length_header(self):
        if self.content_length:
            return ("Content-Length", str(self.content_length))
