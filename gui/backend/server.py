from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys

# Add parent directory to path to import Controller and Executor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from controller import Controller
from executor import Executor
from api_proxy import get_status, get_progress, get_phases, get_log

BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

# Initialize components
controller = Controller()
executor = Executor()

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
                intent_packet = json.loads(post_data)
                
                # 1. Basic Envelope Validation
                required = ["command_id", "intent", "timestamp", "params"]
                if not all(k in intent_packet for k in required):
                    return self.respond_error(400, "Missing required fields in intent envelope")

                # 2. Get Current State
                current_state = get_status()

                # 3. Consult Decision Core (Single Authority)
                decision = controller.decide(intent_packet, current_state)

                # 4. Audit Log Decision
                print(f"[AUDIT] {intent_packet['timestamp']} | {intent_packet['command_id']} | {intent_packet['intent']} | Decision: {decision['accepted']} | Next Stage: {decision['next_stage']}")

                if not decision["accepted"]:
                    return self.respond_error(403, decision["reason"])

                # 5. Execution Isolation Layer (Only if decision is accepted)
                execution_report = executor.execute(decision)
                
                # 6. Audit Log Execution
                print(f"[AUDIT] {execution_report['timestamp']} | {execution_report['execution_id']} | Stage: {execution_report['stage']} | Status: {execution_report['status']}")

                # 7. Respond with combined report
                self.respond_json({
                    "ok": True,
                    "decision": decision,
                    "execution": execution_report
                })

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
