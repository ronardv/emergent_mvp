import json
import shutil
from pathlib import Path
from datetime import datetime

class SandboxContext:
    def __init__(self, project_root="projects/default", sandbox_root="runtime/sandbox"):
        self.project_root = Path(project_root)
        self.sandbox_root = Path(sandbox_root)
        self.state_path = Path("runtime/state.json")
        
    def is_enabled(self):
        state = self._load_state()
        return state.get("sandbox_mode", False)

    def set_enabled(self, enabled: bool):
        state = self._load_state()
        state["sandbox_mode"] = enabled
        if enabled:
            self._initialize_sandbox()
        self._save_state(state)
        return {"status": "SUCCESS", "sandbox_mode": enabled}

    def _initialize_sandbox(self):
        """
        Copy production files to sandbox for isolated work.
        """
        if self.sandbox_root.exists():
            shutil.rmtree(self.sandbox_root)
        
        self.sandbox_root.mkdir(parents=True, exist_ok=True)
        prod_files = self.project_root / "files"
        if prod_files.exists():
            shutil.copytree(prod_files, self.sandbox_root / "files")
        
        print(f"[SANDBOX] Initialized isolated context at {self.sandbox_root}")

    def get_active_path(self, relative_path):
        """
        Returns sandbox path if enabled, otherwise production path.
        """
        if self.is_enabled():
            return self.sandbox_root / relative_path
        return self.project_root / relative_path

    def promote_to_production(self):
        """
        Apply sandbox changes to production.
        """
        if not self.is_enabled():
            return {"status": "ERROR", "reason": "Sandbox not enabled"}
            
        sandbox_files = self.sandbox_root / "files"
        prod_files = self.project_root / "files"
        
        if sandbox_files.exists():
            if prod_files.exists():
                shutil.rmtree(prod_files)
            shutil.copytree(sandbox_files, prod_files)
            
        print("[SANDBOX] Promoted sandbox results to production.")
        return {"status": "SUCCESS", "timestamp": datetime.utcnow().isoformat() + "Z"}

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
