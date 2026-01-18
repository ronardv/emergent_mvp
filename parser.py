class Parser:
    def parse(self, text: str) -> dict:
        parts = text.strip().split()
        if not parts:
            raise RuntimeError("Empty command")

        command = parts[0]
        target = parts[1] if len(parts) > 1 else None

        return {
            "command": command,
            "target": target
        }
