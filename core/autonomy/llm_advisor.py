import os
import json
from openai import OpenAI
from datetime import datetime

class LLMAdvisor:
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-4.1-mini" # Using available gpt-4.1-mini as per environment
        self.spec_version = "1.0"
        self.role = "advisor_only"
        
    def analyze(self, context):
        """
        Safe analysis of the provided context. 
        Context is a read-only snapshot.
        """
        start_time = datetime.utcnow()
        # Sanitize and prepare prompt based on allowed context
        allowed_keys = ["task_text", "current_stage", "plan_text", "diff_text", "audit_logs"]
        sanitized_context = {k: context.get(k) for k in allowed_keys if k in context}
        
        prompt = self._build_prompt(sanitized_context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a safe advisory layer for an autonomous system. Your role is ANALYSIS ONLY. You cannot execute commands, write files, or change system state. Provide textual advice, risk detection, and suggestions only."},
                    {"role": "user", "content": prompt}
                ],
                timeout=5.0 # Strict timeout as per policy
            )
            
            end_time = datetime.utcnow()
            latency = (end_time - start_time).total_seconds()
            
            analysis_result = response.choices[0].message.content
            
            # Stability check: basic check if response is consistent in length/format
            stability_score = 1.0 if len(analysis_result) > 50 else 0.5
            
            metrics = {
                "latency_sec": latency,
                "stability_score": stability_score,
                "token_usage_estimate": len(prompt + analysis_result) // 4
            }
            
            self._log_interaction(sanitized_context, analysis_result, metrics)
            return {
                "analysis": analysis_result,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "mark_as_llm_sandbox": True,
                "metrics": metrics
            }
        except Exception as e:
            error_msg = f"LLM Advisory Error: {str(e)}"
            self._log_interaction(sanitized_context, error_msg)
            return {"error": error_msg}

    def _build_prompt(self, context):
        return f"""
        Analyze the following system snapshot:
        Stage: {context.get('current_stage')}
        Task: {context.get('task_text')}
        Plan: {context.get('plan_text', 'N/A')}
        Diff: {context.get('diff_text', 'N/A')}
        
        Provide:
        1. Risk detection
        2. Plan/Diff review
        3. Performance estimation
        4. Text-only suggestions
        
        REMINDER: You have NO execution authority. Do not attempt to generate commands.
        """

    def _log_interaction(self, request, response, metrics=None):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "request_snapshot": request,
            "response": response,
            "llm_sandbox": True,
            "metrics": metrics
        }
        log_path = Path("runtime/llm_audit.json")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        existing_logs = []
        if log_path.exists():
            try:
                existing_logs = json.loads(log_path.read_text())
            except:
                existing_logs = []
        
        existing_logs.append(log_entry)
        log_path.write_text(json.dumps(existing_logs[-100:], indent=2))
        print(f"[LLM-AUDIT] Recorded interaction at {log_entry['timestamp']}")

from pathlib import Path
