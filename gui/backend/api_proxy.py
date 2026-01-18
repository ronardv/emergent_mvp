def get_status(): return {}
def get_progress(): return {}
def get_phases(): return {}
def get_log(): return {"lines":[]}

def handle_command(data):
    command = data.get("command")
    operator = data.get("operator")
    context = data.get("context", {})
    print(f"Command received: {command} from {operator}")
    return {"status": "accepted"}
