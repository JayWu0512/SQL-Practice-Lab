"""Local, read-only Supabase query runner for sql_tutorial.html.

The server intentionally binds only to 127.0.0.1. Database credentials are
kept in process memory and are never written to disk or returned to the page.
"""

from __future__ import annotations

import json
import re
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, Engine


HOST = "127.0.0.1"
PORT = 8765
ROOT = Path(__file__).resolve().parent
SERVER_VERSION = "placeholder-fix-2"
engine: Engine | None = None

FORBIDDEN_SQL = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|COPY|GRANT|REVOKE|TRUNCATE|VACUUM)\b",
    re.IGNORECASE,
)
PASSWORD_PLACEHOLDER = re.compile(r":\[[^@\]]+\]@")


def json_response(handler: SimpleHTTPRequestHandler, status: int, payload: dict) -> None:
    body = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def read_json(handler: SimpleHTTPRequestHandler) -> dict:
    length = int(handler.headers.get("Content-Length", "0"))
    if length <= 0 or length > 100_000:
        raise ValueError("Request body is missing or too large.")
    return json.loads(handler.rfile.read(length).decode("utf-8"))


def make_engine(connection_url: str, password: str) -> Engine:
    # Supabase's copied URL uses [YOUR-PASSWORD]. Square brackets make
    # Python's URL parser look for an IPv6 host, so replace that display-only
    # placeholder before parsing. The real password comes from the separate
    # local password field and is never written into this URL.
    normalized_url = PASSWORD_PLACEHOLDER.sub(
        ":password-not-used@", connection_url.strip()
    )
    parsed = urlparse(normalized_url)
    if parsed.scheme not in {"postgresql", "postgres"}:
        raise ValueError("Use a PostgreSQL Session pooler URL.")
    if not parsed.username or not parsed.hostname:
        raise ValueError("The connection URL needs a username and host.")
    if parsed.port not in {5432, None}:
        raise ValueError("Use the Session pooler URL on port 5432.")

    database_url = URL.create(
        "postgresql+psycopg",
        username=parsed.username,
        password=password,
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path.lstrip("/") or "postgres",
    )
    return create_engine(
        database_url,
        connect_args={"sslmode": "require"},
        pool_pre_ping=True,
    )


def validate_read_only(sql: str) -> str:
    statement = sql.strip()
    if not statement:
        raise ValueError("Enter a SQL query first.")
    if statement.endswith(";"):
        statement = statement[:-1].strip()
    if ";" in statement:
        raise ValueError("Run one SQL statement at a time.")
    if not re.match(r"^(SELECT|WITH|EXPLAIN)\b", statement, re.IGNORECASE):
        raise ValueError("This runner accepts SELECT, WITH, and EXPLAIN queries only.")
    if FORBIDDEN_SQL.search(statement):
        raise ValueError("Write operations are disabled in this teaching runner.")
    return statement


class TutorialHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: object, **kwargs: object) -> None:
        # Serve the website next to this script even if Python was launched
        # from a different working directory on macOS or Windows.
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        request_path = urlparse(self.path).path
        if request_path in {"/", "/index.html", "/sql_tutorial.html"}:
            self.path = "/sql_tutorial.html"
            return super().do_GET()
        if request_path == "/api/health":
            return json_response(
                self,
                HTTPStatus.OK,
                {"connected": engine is not None, "version": SERVER_VERSION},
            )

        # The website needs its own images, but do not expose arbitrary files
        # from the project folder (for example, this server's source code).
        if request_path.startswith("/assets/"):
            assets_directory = (ROOT / "assets").resolve()
            requested_file = (ROOT / request_path.lstrip("/")).resolve()
            if assets_directory in requested_file.parents and requested_file.is_file():
                self.path = request_path
                return super().do_GET()

        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        global engine
        try:
            payload = read_json(self)
            if self.path == "/api/connect":
                connection_url = str(payload.get("connection_url", ""))
                password = str(payload.get("password", ""))
                if not password:
                    raise ValueError("Enter your database password in the local dialog.")
                new_engine = make_engine(connection_url, password)
                with new_engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                if engine is not None:
                    engine.dispose()
                engine = new_engine
                return json_response(self, HTTPStatus.OK, {"message": "Connected to Supabase."})

            if self.path == "/api/query":
                if engine is None:
                    raise ValueError("Connect to Supabase first.")
                statement = validate_read_only(str(payload.get("sql", "")))
                with engine.connect() as connection:
                    with connection.begin():
                        connection.execute(text("SET TRANSACTION READ ONLY"))
                        connection.execute(text("SET LOCAL statement_timeout = '10s'"))
                        result = connection.execute(text(statement))
                        columns = list(result.keys())
                        rows = [list(row) for row in result.fetchmany(500)]
                return json_response(
                    self,
                    HTTPStatus.OK,
                    {"columns": columns, "rows": rows, "truncated": len(rows) == 500},
                )
            self.send_error(HTTPStatus.NOT_FOUND)
        except (ValueError, json.JSONDecodeError) as error:
            json_response(self, HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except Exception:
            # Avoid returning database connection details or credentials to the browser.
            json_response(
                self,
                HTTPStatus.BAD_GATEWAY,
                {"error": "The database request failed. Check the Session pooler URL, password, and network connection."},
            )

    def log_message(self, _format: str, *_args: object) -> None:
        # Do not log request bodies, which may contain a password.
        return


if __name__ == "__main__":
    print(f"Open http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), TutorialHandler).serve_forever()
