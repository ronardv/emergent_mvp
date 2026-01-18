class DiffBuilder:
    def build(self, old_code: str, kernel_output: dict) -> dict:
        if "new_code" not in kernel_output:
            raise RuntimeError("Kernel output missing new_code")

        return {
            "type": "diff_proposal",
            "target": kernel_output["target"],
            "old_code": old_code,
            "new_code": kernel_output["new_code"]
        }
