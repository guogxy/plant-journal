#!/usr/bin/env python3
"""Local-only GitHub Pages prefix preview, including 404 behavior."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import argparse

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "/plant-journal/"


class Preview(SimpleHTTPRequestHandler):
    def prepare_path(self):
        if self.path in ("/", "/plant-journal"):
            self.send_response(302)
            self.send_header("Location", PREFIX)
            self.end_headers()
            return False
        if not urlparse(self.path).path.startswith(PREFIX):
            self.send_error(404)
            return False
        self.path = self.path[len(PREFIX)-1:]
        return True

    def do_GET(self):
        if self.prepare_path():
            super().do_GET()

    def do_HEAD(self):
        if self.prepare_path():
            super().do_HEAD()

    def send_error(self, code, message=None, explain=None):
        if code != 404:
            return super().send_error(code, message, explain)
        body = (ROOT / "404.html").read_bytes()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def translate_path(self, path):
        # Constrain traversal to Website; SimpleHTTPRequestHandler normalizes dots.
        return super().translate_path(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8767)
    args = parser.parse_args()
    handler = lambda *a, **kw: Preview(*a, directory=str(ROOT), **kw)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"Preview: http://127.0.0.1:{args.port}{PREFIX}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
