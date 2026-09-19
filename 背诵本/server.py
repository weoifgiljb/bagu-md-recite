# -*- coding: utf-8 -*-
"""Local recite server: static files + SQLite progress API."""
from __future__ import annotations

import json
import sqlite3
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent
DB = ROOT / "recite.db"
HOST = "127.0.0.1"
PORT = 8765


def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS progress (
              question_id TEXT PRIMARY KEY,
              status TEXT NOT NULL DEFAULT 'new',
              notes TEXT NOT NULL DEFAULT '',
              updated_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
            )
            """
        )


def all_progress():
    with connect() as conn:
        rows = conn.execute(
            "SELECT question_id, status, notes, updated_at FROM progress"
        ).fetchall()
    return {
        r["question_id"]: {
            "status": r["status"],
            "notes": r["notes"],
            "updated_at": r["updated_at"],
        }
        for r in rows
    }


def upsert(question_id, status=None, notes=None):
    with connect() as conn:
        row = conn.execute(
            "SELECT status, notes FROM progress WHERE question_id=?",
            (question_id,),
        ).fetchone()
        if row is None:
            st = status if status is not None else "new"
            nt = notes if notes is not None else ""
            conn.execute(
                "INSERT INTO progress(question_id, status, notes, updated_at) "
                "VALUES (?,?,?,datetime('now','localtime'))",
                (question_id, st, nt),
            )
        else:
            st = status if status is not None else row["status"]
            nt = notes if notes is not None else row["notes"]
            conn.execute(
                "UPDATE progress SET status=?, notes=?, "
                "updated_at=datetime('now','localtime') WHERE question_id=?",
                (st, nt, question_id),
            )
        conn.commit()
    return {"question_id": question_id, "status": st, "notes": nt}


def bulk_import(items):
    with connect() as conn:
        for qid, val in items.items():
            if not isinstance(val, dict):
                continue
            status = val.get("status") or "new"
            notes = val.get("notes") or ""
            if status not in ("new", "learning", "mastered", "hard"):
                status = "new"
            conn.execute(
                """
                INSERT INTO progress(question_id, status, notes, updated_at)
                VALUES (?,?,?,datetime('now','localtime'))
                ON CONFLICT(question_id) DO UPDATE SET
                  status=excluded.status,
                  notes=excluded.notes,
                  updated_at=datetime('now','localtime')
                """,
                (qid, status, notes),
            )
        conn.commit()
    return {"ok": True, "count": len(items)}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _json(self, code=200, payload=None):
        body = json.dumps(payload if payload is not None else {}, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b"{}"
        try:
            return json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return None

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            return self._json(200, {"ok": True, "db": str(DB)})
        if path == "/api/progress":
            return self._json(200, {"items": all_progress()})
        if path in ("/", "/index.html"):
            self.path = "/index.html"
        return super().do_GET()

    def do_PUT(self):
        path = urlparse(self.path).path
        data = self._read_json()
        if data is None:
            return self._json(400, {"error": "invalid json"})
        if path.startswith("/api/progress/"):
            qid = unquote(path[len("/api/progress/"):])
            if not qid:
                return self._json(400, {"error": "missing id"})
            status = data.get("status")
            notes = data.get("notes")
            if status is not None and status not in ("new", "learning", "mastered", "hard"):
                return self._json(400, {"error": "bad status"})
            return self._json(200, upsert(qid, status=status, notes=notes))
        return self._json(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        data = self._read_json()
        if data is None:
            return self._json(400, {"error": "invalid json"})
        if path == "/api/progress/import":
            items = data.get("items") or {}
            if not isinstance(items, dict):
                return self._json(400, {"error": "items must be object"})
            return self._json(200, bulk_import(items))
        return self._json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        msg = fmt % args
        if "GET /api/health" in msg:
            return
        print(msg)


def main():
    init_db()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}/index.html"
    print("Recite server:", url)
    print("SQLite:", DB)
    print("Close this window to stop.")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("stopped")


if __name__ == "__main__":
    main()
