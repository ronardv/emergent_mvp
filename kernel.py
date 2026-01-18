class Kernel:
    def process(self, action: dict, project_files: dict) -> dict:
        if action["command"] == "analyze":
            return {
                "intent": "NO_CHANGE",
                "summary": "Analysis complete"
            }

        if action["command"] == "modify":
            target = action["target"]
            old_code = project_files.get(target, "")
            new_code = old_code + "\n// Modified by Emergent\n"

            return {
                "intent": "MODIFY_FILE",
                "target": target,
                "new_code": new_code
            }

        raise RuntimeError("Unsupported command")
