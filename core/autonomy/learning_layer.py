import json
from pathlib import Path
from datetime import datetime

class LearningLayer:
    def __init__(self, storage_path="runtime/learning_data.json"):
        self.storage_path = Path(storage_path)
        self.mode = "passive_plus"
        
    def record_event(self, event_type, data):
        """
        Passive learning from system events.
        """
        if event_type not in ["approved_plan", "approved_diff", "operator_acceptance", "rollback"]:
            return
            
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "data_summary": self._summarize(data)
        }
        
        self._append_entry(entry)
        print(f"[LEARNING] Recorded {event_type} pattern.")

    def _summarize(self, data):
        # Simple summary logic for passive learning
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if k in ["stage", "intent", "status"]}
        return str(data)

    def _append_entry(self, entry):
        data = []
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
            except:
                data = []
        
        data.append(entry)
        # Keep only last 1000 entries
        data = data[-1000:]
        
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.storage_path.write_text(json.dumps(data, indent=2))
