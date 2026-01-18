import json
from datetime import datetime

class Validator:
    def __init__(self):
        self.INVARIANTS = [
            {"id": "NO_AUTONOMOUS_EXECUTION", "rule": "System must not execute without explicit operator intent"},
            {"id": "CONTROLLER_FINAL_AUTHORITY", "rule": "No component may bypass controller decisions"},
            {"id": "GUI_OBSERVATION_ONLY", "rule": "GUI must not contain decision or execution logic"}
        ]

    def enforce_constitution(self, context, action_type):
        """
        Final invariant enforcement layer.
        context: dict containing relevant data for the check
        action_type: 'before_decision_accept' | 'before_execution_start' | 'before_apply_commit'
        """
        # 1. NO_AUTONOMOUS_EXECUTION
        if action_type == 'before_execution_start':
            if not context.get('operator_intent_verified'):
                return self._halt("NO_AUTONOMOUS_EXECUTION violation: Missing operator intent verification")

        # 2. CONTROLLER_FINAL_AUTHORITY
        if action_type in ['before_execution_start', 'before_apply_commit']:
            if not context.get('decision_packet') or not context['decision_packet'].get('accepted'):
                return self._halt("CONTROLLER_FINAL_AUTHORITY violation: No accepted decision packet found")

        # 3. GUI_OBSERVATION_ONLY
        if action_type == 'before_decision_accept':
            if context.get('gui_decision_detected'):
                return self._halt("GUI_OBSERVATION_ONLY violation: Decision logic detected in GUI request")

        return {"status": "PASS", "timestamp": datetime.utcnow().isoformat() + "Z"}

    def _halt(self, reason):
        print(f"[CRITICAL_HALT] {reason}")
        return {
            "status": "HALT",
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "require_operator_ack": True
        }

    # Legacy methods kept for compatibility
    def validate_action(self, action, state): pass
    def validate_kernel_output(self, output): pass
    def validate_diff(self, diff): pass
    def validate_transition(self, current_phase, action): pass
