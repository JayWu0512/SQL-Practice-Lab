"""Vercel's required Python entrypoint and static tutorial handler."""

from __future__ import annotations

import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

from api import health, query


ROOT = Path(__file__).resolve().parent.parent
ASSETS = (ROOT / "assets").resolve()


def json_response(handler: BaseHTTPRequestHandler, status: HTTPStatus, payload: dict) -> None:
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        request_path = urlparse(self.path).path
        if request_path == "/api/health":
            return health.handler.do_GET(self)

        if request_path in {"/", "/sql_tutorial.html"}:
            return self.serve_file(ROOT / "sql_tutorial.html")

        if request_path.startswith("/assets/"):
            requested_file = (ROOT / request_path.lstrip("/")).resolve()
            if ASSETS in requested_file.parents and requested_file.is_file():
                return self.serve_file(requested_file)

        return json_response(self, HTTPStatus.NOT_FOUND, {"error": "Not found."})

    def do_POST(self) -> None:
        if urlparse(self.path).path == "/api/query":
            return query.handler.do_POST(self)
        return json_response(self, HTTPStatus.NOT_FOUND, {"error": "Not found."})

    def serve_file(self, file_path: Path) -> None:
        body = file_path.read_bytes()
        content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        if content_type.startswith("text/"):
            content_type += "; charset=utf-8"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "public, max-age=3600")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format: str, *_args: object) -> None:
        return
