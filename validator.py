import json
from pathlib import Path

class Validator:
    def __init__(self):
        base = Path("config")
        self.constitution = json.loads((base / "constitution.json").read_text())
        self.dsl = json.loads((base / "command_dsl.json").read_text())

    def validate_action(self, action, state):
        cmd = action["command"]
        if cmd not in self.dsl["commands"]:
            raise RuntimeError("Unknown command")

        allowed = self.dsl["commands"][cmd]["allowed_phases"]
        if state["current_phase"] not in allowed:
            raise RuntimeError("Command not allowed in this phase")

    def validate_kernel_output(self, output):
        if "intent" not in output:
            raise RuntimeError("Invalid kernel output")

    def validate_diff(self, diff):
        if diff["old_code"] == diff["new_code"]:
            raise RuntimeError("Empty diff")

    def validate_transition(self, current_phase, action):
        transitions = self.constitution["transitions"]
        cmd = action["command"]

        if cmd == "analyze":
            target = "ANALYZE"
        elif cmd == "modify":
            target = "EXECUTE"
        else:
            raise RuntimeError("No transition rule")

        if target not in transitions[current_phase]:
            raise RuntimeError("Illegal phase transition")

        return target
