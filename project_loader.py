from pathlib import Path

class Project:
    def __init__(self, root: Path):
        self.root = root
        self.files = self._load_files()

    def _load_files(self):
        files_dir = self.root / "files"
        result = {}
        for path in files_dir.glob("*"):
            result[path.name] = path.read_text(encoding="utf-8")
        return result
