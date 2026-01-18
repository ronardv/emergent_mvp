def run_advisor(user_input=None, current_phase=None, last_action=None):
    """
    SPEC v1.9
    Read-only advisory component.
    No side effects.
    """

    return {
        "analysis": f"Advisory analysis for phase {current_phase}",
        "risks": [],
        "suggestions": [],
        "confidence": 0.5
    }
