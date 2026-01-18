from core.autonomy.llm_advisor import LLMAdvisor

def run_advisor(user_input=None, current_phase=None, last_action=None, extra_context=None):
    """
    SPEC v1.10 (LLM Sandbox Policy v1.0)
    Read-only advisory component with LLM support.
    No side effects.
    """
    
    context = {
        "task_text": user_input,
        "current_stage": current_phase,
        "intent": last_action
    }
    if extra_context:
        context.update(extra_context)

    # Attempt LLM Analysis if enabled
    llm = LLMAdvisor()
    llm_result = llm.analyze(context)
    
    if "error" not in llm_result:
        return {
            "analysis": llm_result["analysis"],
            "risks": ["LLM-detected risks included in analysis"],
            "suggestions": ["See LLM analysis for suggestions"],
            "confidence": 0.8,
            "llm_enhanced": True
        }

    # Fallback to basic analysis
    return {
        "analysis": f"Basic advisory analysis for phase {current_phase}. LLM unavailable.",
        "risks": [],
        "suggestions": [],
        "confidence": 0.5,
        "llm_enhanced": False
    }
