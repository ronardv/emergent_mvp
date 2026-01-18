import uuid
from datetime import datetime
from core.audit.audit_trail import AuditTrail

class Controller:
    def __init__(self, parser=None, validator=None, kernel=None, executor=None):
        # Dependencies kept for compatibility
        self.parser = parser
        self.validator = validator
        self.kernel = kernel
        self.executor = executor
        
        # Stage 8: Audit Trail Activation
        self.audit_trail = AuditTrail()
        
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
        Deterministic decision core with Audit Trail.
        """
        intent = intent_packet.get("intent")
        current_stage = current_state.get("stage", "IDLE")
        decision_id = str(uuid.uuid4())
        command_id = intent_packet.get("command_id")
        params = intent_packet.get("params", {})
        
        # Audit: INTENT_RECEIVED
        self.audit_trail.log(command_id, intent, params, "RECEIVED")
        
        # 1. Validate Intent exists
        if intent not in self.TRANSITIONS:
            decision = self._make_decision(decision_id, False, f"Unknown intent: {intent}", current_stage, False)
            self.audit_trail.log(command_id, intent, params, "REJECTED: UNKNOWN_INTENT")
            return decision
            
        # 2. Validate Stage Transition
        transition = self.TRANSITIONS[intent]
        if current_stage not in transition["from"]:
            decision = self._make_decision(decision_id, False, f"Intent {intent} not allowed in stage {current_stage}", current_stage, False)
            self.audit_trail.log(command_id, intent, params, "REJECTED: INVALID_STAGE")
            return decision
            
        # 3. Formulate Decision
        next_stage = transition["to"]
        decision = self._make_decision(decision_id, True, "Intent accepted", next_stage, True)
        
        # Audit: INTENT_ACCEPTED
        self.audit_trail.log(command_id, intent, params, f"ACCEPTED: NEXT_STAGE={next_stage}")
        
        return decision

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
        pass
