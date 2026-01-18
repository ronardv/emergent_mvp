import shutil
from pathlib import Path

class Executor:
    def apply_diff(self, diff: dict, project_root: Path):
        target = project_root / "files" / diff["target"]

        backup = target.with_suffix(".bak")
        shutil.copy(target, backup)

        target.write_text(diff["new_code"], encoding="utf-8")

        return {
            "status": "applied",
            "backup": str(backup)
        }
