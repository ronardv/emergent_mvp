from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import uuid
from datetime import datetime
from api_proxy import get_status, get_progress, get_phases, get_log

BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

ALLOWED_INTENTS = {
    "START_ANALYSIS": {"allowed_stage": ["IDLE", "INIT"]},
    "STOP_EXECUTION": {"allowed_stage": ["ANALYZE", "PLAN", "DIFF", "APPLY"]},
    "REQUEST_PLAN": {"allowed_stage": ["ANALYZE_COMPLETE"]},
    "REQUEST_DIFF": {"allowed_stage": ["PLAN_COMPLETE"]},
    "APPLY_DIFF": {"allowed_stage": ["DIFF_COMPLETE"]},
    "ROLLBACK": {"allowed_stage": ["APPLY_COMPLETE"]}
}

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/api/status": self.respond_json(get_status())
        elif self.path == "/api/progress": self.respond_json(get_progress())
        elif self.path == "/api/phases": self.respond_json(get_phases())
        elif self.path == "/api/log": self.respond_json(get_log())
        elif self.path == "/" or self.path == "/index.html": self.serve_file("index.html", "text/html")
        elif self.path.endswith(".css"): self.serve_file(self.path.lstrip("/"), "text/css")
        elif self.path.endswith(".js"): self.serve_file(self.path.lstrip("/"), "application/javascript")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/intent":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                # 1. Validate Envelope
                required = ["command_id", "intent", "timestamp", "params"]
                if not all(k in data for k in required):
                    return self.respond_error(400, "Missing required fields")

                intent_name = data["intent"]
                if intent_name not in ALLOWED_INTENTS:
                    return self.respond_error(400, f"Unknown intent: {intent_name}")

                # 2. Validate Stage
                current_stage = get_status().get("stage", "IDLE")
                allowed_stages = ALLOWED_INTENTS[intent_name]["allowed_stage"]
                if current_stage not in allowed_stages:
                    return self.respond_error(403, f"Intent {intent_name} not allowed in stage {current_stage}")

                # 3. Validate Params (START_ANALYSIS specific)
                if intent_name == "START_ANALYSIS":
                    task_text = data["params"].get("task_text")
                    if not task_text or len(task_text) < 1:
                        return self.respond_error(400, "Invalid params: task_text required")

                # 4. Audit Log
                print(f"[AUDIT] {data['timestamp']} | {data['command_id']} | {intent_name} | Params Hash: {hash(str(data['params']))}")

                # 5. Respond (Logic stub)
                self.respond_json({"ok": True, "status": "accepted", "command_id": data["command_id"]})

            except Exception as e:
                self.respond_error(500, str(e))
        else:
            self.send_response(404)
            self.end_headers()

    def serve_file(self, filename, content_type):
        file_path = os.path.join(FRONTEND_DIR, filename)
        if not os.path.isfile(file_path):
            self.send_response(404); self.end_headers(); return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        with open(file_path, "rb") as f: self.wfile.write(f.read())

    def respond_json(self, payload):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def respond_error(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": False, "error": message}).encode())

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
