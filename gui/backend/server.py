from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from api_proxy import get_status, get_progress, get_phases, get_log

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status": self.respond(get_status())
        elif self.path == "/api/progress": self.respond(get_progress())
        elif self.path == "/api/phases": self.respond(get_phases())
        elif self.path == "/api/log": self.respond(get_log())
        else:
            self.send_response(404); self.end_headers()

    def respond(self, payload):
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

HTTPServer(("0.0.0.0",8080),Handler).serve_forever()
