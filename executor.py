import uuid
from datetime import datetime

class Executor:
    def __init__(self):
        self.MODES = {
            "ANALYZE": "read_only",
            "PLAN": "simulation_only",
            "DIFF": "diff_generation_only",
            "APPLY": "sandboxed_apply"
        }

    def execute(self, decision_packet):
        """
        Isolated execution logic.
        Requires an accepted decision_packet from the controller.
        """
        # 1. Validate decision packet
        if not decision_packet.get("accepted") or not decision_packet.get("execution_allowed"):
            raise PermissionError("Execution denied: decision packet not accepted or execution not allowed")

        stage = decision_packet.get("next_stage")
        execution_id = str(uuid.uuid4())
        
        # 2. Determine execution mode
        mode = self.MODES.get(stage, "restricted")
        
        # 3. Perform isolated action based on stage
        artifacts = []
        side_effects = "none"
        
        if stage == "ANALYZE":
            # read_only simulation
            artifacts.append("file_structure_map.json")
        elif stage == "PLAN":
            # simulation_only
            artifacts.append("execution_plan.md")
        elif stage == "DIFF":
            # diff_generation_only
            artifacts.append("changeset.diff")
        elif stage == "APPLY":
            # sandboxed_apply simulation
            artifacts.append("apply_report.json")
            side_effects = "filesystem_mutation_simulated"
            
        return self._make_report(execution_id, stage, "success", artifacts, side_effects)

    def _make_report(self, execution_id, stage, status, artifacts, side_effects):
        return {
            "execution_id": execution_id,
            "stage": stage,
            "status": status,
            "artifacts_generated": artifacts,
            "side_effects_detected": side_effects,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def apply_diff(self, diff, project_root):
        # Legacy method kept for backward compatibility
        pass
