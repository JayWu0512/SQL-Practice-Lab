"""Read-only SQL endpoint for the Vercel deployment.

Connection values stay in Vercel environment variables. The endpoint accepts
one SELECT, WITH, or EXPLAIN statement and never returns database credentials.
"""

from __future__ import annotations

import json
import os
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.pool import NullPool


MAX_BODY_BYTES = 100_000
MAX_ROWS = 500
FORBIDDEN_SQL = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|COPY|GRANT|REVOKE|TRUNCATE|VACUUM)\b",
    re.IGNORECASE,
)
PASSWORD_PLACEHOLDER = re.compile(r":\[[^@\]]+\]@")


def json_response(handler: BaseHTTPRequestHandler, status: HTTPStatus, payload: dict) -> None:
    body = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


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


def make_engine():
    connection_url = os.environ.get("SUPABASE_CONNECTION_URL", "")
    password = os.environ.get("SUPABASE_DATABASE_PASSWORD", "")
    if not connection_url or not password:
        raise RuntimeError("The course database is not configured.")

    normalized_url = PASSWORD_PLACEHOLDER.sub(":password-not-used@", connection_url)
    parsed = urlparse(normalized_url)
    if parsed.scheme not in {"postgresql", "postgres"}:
        raise RuntimeError("The course database URL is invalid.")
    if not parsed.username or not parsed.hostname or parsed.port not in {5432, 6543}:
        raise RuntimeError("The course database URL is invalid.")

    database_url = URL.create(
        "postgresql+psycopg",
        username=parsed.username,
        password=password,
        host=parsed.hostname,
        port=parsed.port,
        database=parsed.path.lstrip("/") or "postgres",
    )
    # A serverless function must not keep a database connection between
    # invocations. Supabase's Transaction pooler shares short-lived clients.
    return create_engine(
        database_url,
        connect_args={"sslmode": "require", "prepare_threshold": None},
        poolclass=NullPool,
    )


class handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if os.environ.get("LAB_ENABLED", "").lower() != "true":
            return json_response(
                self,
                HTTPStatus.SERVICE_UNAVAILABLE,
                {"error": "The course SQL runner is currently closed."},
            )

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY_BYTES:
                raise ValueError("Request body is missing or too large.")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            statement = validate_read_only(str(payload.get("sql", "")))

            engine = make_engine()
            try:
                with engine.connect() as connection:
                    with connection.begin():
                        connection.execute(text("SET TRANSACTION READ ONLY"))
                        connection.execute(text("SET LOCAL statement_timeout = '8s'"))
                        result = connection.execute(text(statement))
                        columns = list(result.keys())
                        rows = [list(row) for row in result.fetchmany(MAX_ROWS)]
            finally:
                engine.dispose()

            return json_response(
                self,
                HTTPStatus.OK,
                {"columns": columns, "rows": rows, "truncated": len(rows) == MAX_ROWS},
            )
        except (ValueError, json.JSONDecodeError) as error:
            return json_response(self, HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except RuntimeError as error:
            return json_response(self, HTTPStatus.SERVICE_UNAVAILABLE, {"error": str(error)})
        except Exception:
            return json_response(
                self,
                HTTPStatus.BAD_GATEWAY,
                {"error": "The database request failed. Please try again later."},
            )

    def do_GET(self) -> None:
        return json_response(self, HTTPStatus.METHOD_NOT_ALLOWED, {"error": "Use POST."})

    def log_message(self, _format: str, *_args: object) -> None:
        return
