from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from api_proxy import get_status, get_progress, get_phases, get_log

BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # --- API ---
        if self.path == "/api/status":
            self.respond_json(get_status())
        elif self.path == "/api/progress":
            self.respond_json(get_progress())
        elif self.path == "/api/phases":
            self.respond_json(get_phases())
        elif self.path == "/api/log":
            self.respond_json(get_log())

        # --- GUI ---
        elif self.path == "/" or self.path == "/index.html":
            self.serve_file("index.html", "text/html")

        elif self.path.endswith(".css"):
            self.serve_file(self.path.lstrip("/"), "text/css")

        elif self.path.endswith(".js"):
            self.serve_file(self.path.lstrip("/"), "application/javascript")

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path in ["/api/start", "/api/stop", "/api/apply", "/api/rollback"]:
            # Logic not implemented yet, return 501 as per requirements
            self.send_response(501)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "message": "Not implemented"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def serve_file(self, filename, content_type):
        file_path = os.path.join(FRONTEND_DIR, filename)
        if not os.path.isfile(file_path):
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        with open(file_path, "rb") as f:
            self.wfile.write(f.read())

    def respond_json(self, payload):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
