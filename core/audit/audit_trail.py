from datetime import datetime
import hashlib

class AuditTrail:
    def __init__(self):
        self.records = []

    def log(self, command_id, intent, params, result, autonomous=False, sandbox=False):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "command_id": command_id,
            "intent": intent,
            "params_hash": self._hash(params),
            "result": result,
            "autonomous": autonomous,
            "sandbox": sandbox
        }
        self.records.append(entry)
        if autonomous:
            tag = "[AUDIT-SANDBOX]" if sandbox else "[AUDIT-AUTONOMY]"
            print(f"{tag} {entry['timestamp']} | {command_id} | {intent} | Result: {result}")

    def _hash(self, params):
        return hashlib.sha256(str(params).encode()).hexdigest()
