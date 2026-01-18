import json
from pathlib import Path
from datetime import datetime

class AutonomyManager:
    def __init__(self, state_path="runtime/state.json"):
        self.state_path = Path(state_path)
        self.spec_version = "2.1"
        self.allowed_stages = ["ANALYZE", "PLAN", "DIFF"]
        
    def get_status(self):
        state = self._load_state()
        return state.get("autonomy_enabled", False)

    def set_status(self, enabled: bool):
        state = self._load_state()
        state["autonomy_enabled"] = enabled
        state["autonomy_updated_at"] = datetime.utcnow().isoformat() + "Z"
        self._save_state(state)
        return {"status": "SUCCESS", "autonomy_enabled": enabled}

    def can_execute_autonomously(self, current_stage):
        if not self.get_status():
            return False
        return current_stage in self.allowed_stages

    def _load_state(self):
        if not self.state_path.exists():
            return {}
        try:
            return json.loads(self.state_path.read_text())
        except:
            return {}

    def _save_state(self, state):
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(state, indent=2))
