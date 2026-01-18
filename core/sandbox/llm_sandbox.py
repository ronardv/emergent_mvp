import json
from pathlib import Path
from datetime import datetime
from core.autonomy.llm_advisor import LLMAdvisor

class LLMSandbox:
    def __init__(self, state_path="runtime/state.json"):
        self.state_path = Path(state_path)
        self.advisor = LLMAdvisor()
        self.spec_version = "1.0"
        
    def is_enabled(self):
        state = self._load_state()
        return state.get("llm_sandbox_enabled", False)

    def set_enabled(self, enabled: bool):
        state = self._load_state()
        state["llm_sandbox_enabled"] = enabled
        state["llm_sandbox_updated_at"] = datetime.utcnow().isoformat() + "Z"
        self._save_state(state)
        return {"status": "SUCCESS", "llm_sandbox_enabled": enabled}

    def analyze_context(self, context):
        """
        Advisory-only analysis. No execution rights.
        """
        if not self.is_enabled():
            return {"error": "LLM Sandbox is disabled"}
            
        # Ensure read-only by not passing any mutable objects or handles
        # LLMAdvisor already handles sanitization
        return self.advisor.analyze(context)

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
