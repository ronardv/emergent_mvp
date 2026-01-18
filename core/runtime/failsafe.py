import json
from pathlib import Path

class FailSafe:
    def __init__(self, state_path="runtime/state.json"):
        self.armed = True
        self.state_path = Path(state_path)

    def check(self, condition):
        if self.armed and condition:
            return False
        return True

    def validate_autonomy(self, current_stage):
        """
        Ensures autonomy is only active in allowed stages and 
        automatically disables it on violation.
        """
        if not self.state_path.exists():
            return True
            
        try:
            state = json.loads(self.state_path.read_text())
            if state.get("autonomy_enabled"):
                allowed_stages = ["ANALYZE", "PLAN", "DIFF"]
                if current_stage not in allowed_stages:
                    # Violation detected: Auto-disable autonomy
                    state["autonomy_enabled"] = False
                    state["violation_detected"] = True
                    state["violation_reason"] = f"Autonomy active in forbidden stage: {current_stage}"
                    self.state_path.write_text(json.dumps(state, indent=2))
                    print(f"[FAILSAFE] Autonomy disabled due to violation: {current_stage}")
                    return False
        except:
            pass
        return True
