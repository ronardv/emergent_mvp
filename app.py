import json
from pathlib import Path
from parser import Parser
from validator import Validator
from kernel import Kernel
from executor import Executor
from controller import Controller
from project_loader import Project

STATE_FILE = Path("runtime/state.json")

def load_state():
    return json.loads(STATE_FILE.read_text())

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def main():
    parser = Parser()
    validator = Validator()
    kernel = Kernel()
    executor = Executor()
    controller = Controller(parser, validator, kernel, executor)

    project = Project(Path("projects/default"))
    state = load_state()

    print("Emergent MVP started.")
    print("Current state:", state)

    while True:
        cmd = input("> ")
        state, result, advisor_output = controller.handle(cmd, state, project)
        save_state(state)
        print("State:", state)
        if result:
            print("Result:", result)

        print(advisor_output)

if __name__ == "__main__":
    main()
