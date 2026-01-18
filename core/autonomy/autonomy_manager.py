import json
from pathlib import Path
from datetime import datetime

class AutonomyManager:
    def __init__(self, state_path="runtime/state.json"):
        self.state_path = Path(state_path)
        self.spec_version = "1.1"
        self.policy_name = "autonomy_mode_policy"
        
        # Internal mapping as per spec 1.1
        self.MODE_MAPPING = {
            "E2": {
                "internal_mode": "E2",
                "autonomy": False,
                "learning": False
            },
            "E3": {
                "internal_mode": "E3_MAX_PLUS",
                "autonomy": True,
                "learning": True
            }
        }
        self.allowed_stages = ["ANALYZE", "PLAN", "DIFF", "APPLY"]

    def get_current_mode(self):
        state = self._load_state()
        return state.get("gui_mode", "E2")

    def get_internal_config(self):
        gui_mode = self.get_current_mode()
        return self.MODE_MAPPING.get(gui_mode, self.MODE_MAPPING["E2"])

    def set_mode(self, gui_mode: str):
        if gui_mode not in self.MODE_MAPPING:
            return {"status": "ERROR", "reason": f"Invalid mode: {gui_mode}"}
        
        state = self._load_state()
        config = self.MODE_MAPPING[gui_mode]
        
        state["gui_mode"] = gui_mode
        state["internal_mode"] = config["internal_mode"]
        state["autonomy_enabled"] = config["autonomy"]
        state["learning_enabled"] = config["learning"]
        state["policy_version"] = self.spec_version
        state["updated_at"] = datetime.utcnow().isoformat() + "Z"
        
        self._save_state(state)
        return {
            "status": "SUCCESS", 
            "gui_mode": gui_mode, 
            "internal_mode": config["internal_mode"]
        }

    def can_execute_autonomously(self, current_stage):
        config = self.get_internal_config()
        if not config["autonomy"]:
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
