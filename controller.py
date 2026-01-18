from copy import copy
from diff_builder import DiffBuilder
from advisor import run_advisor

class Controller:
    def __init__(self, parser, validator, kernel, executor):
        self.parser = parser
        self.validator = validator
        self.kernel = kernel
        self.executor = executor
        self.diff_builder = DiffBuilder()

    def handle(self, user_input, state, project):
        action = self.parser.parse(user_input)
        self.validator.validate_action(action, state)

        kernel_output = self.kernel.process(action, project.files)
        advisor_output = run_advisor(copy(kernel_output))
        self.validator.validate_kernel_output(kernel_output)

        result = None
        if kernel_output.get("intent") == "MODIFY_FILE":
            old = project.files[kernel_output["target"]]
            diff = self.diff_builder.build(old, kernel_output)
            self.validator.validate_diff(diff)
            result = self.executor.apply_diff(diff, project.root)

        next_phase = self.validator.validate_transition(
            state["current_phase"], action
        )

        new_state = {
            "current_phase": next_phase,
            "history": state["history"] + [action["command"]]
        }

        return new_state, result, advisor_output
