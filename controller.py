import uuid
from datetime import datetime

class Controller:
    def __init__(self, parser=None, validator=None, kernel=None, executor=None):
        # Dependencies kept for compatibility, but core logic is now deterministic
        self.parser = parser
        self.validator = validator
        self.kernel = kernel
        self.executor = executor
        
        self.STAGES = [
            "IDLE", "ANALYZE", "ANALYZE_COMPLETE", "PLAN", "PLAN_COMPLETE",
            "DIFF", "DIFF_COMPLETE", "APPLY", "APPLY_COMPLETE", "HALTED"
        ]
        
        self.TRANSITIONS = {
            "START_ANALYSIS": {"from": ["IDLE", "INIT"], "to": "ANALYZE"},
            "STOP_EXECUTION": {"from": ["ANALYZE", "PLAN", "DIFF", "APPLY"], "to": "HALTED"},
            "REQUEST_PLAN": {"from": ["ANALYZE_COMPLETE"], "to": "PLAN"},
            "REQUEST_DIFF": {"from": ["PLAN_COMPLETE"], "to": "DIFF"},
            "APPLY_DIFF": {"from": ["DIFF_COMPLETE"], "to": "APPLY"},
            "ROLLBACK": {"from": ["APPLY_COMPLETE"], "to": "IDLE"}
        }

    def decide(self, intent_packet, current_state):
        """
        Deterministic decision core.
        Input: intent_packet (dict), current_state (dict)
        Output: decision_packet (dict)
        """
        intent = intent_packet.get("intent")
        current_stage = current_state.get("stage", "IDLE")
        decision_id = str(uuid.uuid4())
        
        # 1. Validate Intent exists in transitions
        if intent not in self.TRANSITIONS:
            return self._make_decision(decision_id, False, f"Unknown intent: {intent}", current_stage, False)
            
        # 2. Validate Stage Transition
        transition = self.TRANSITIONS[intent]
        if current_stage not in transition["from"]:
            return self._make_decision(decision_id, False, f"Intent {intent} not allowed in stage {current_stage}", current_stage, False)
            
        # 3. Formulate Decision
        next_stage = transition["to"]
        return self._make_decision(decision_id, True, "Intent accepted", next_stage, True)

    def _make_decision(self, decision_id, accepted, reason, next_stage, execution_allowed):
        return {
            "decision_id": decision_id,
            "accepted": accepted,
            "reason": reason,
            "next_stage": next_stage,
            "execution_allowed": execution_allowed,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def handle(self, user_input, state, project):
        # Legacy handle method kept for backward compatibility if needed
        # In the new model, the backend calls .decide() directly
        pass
