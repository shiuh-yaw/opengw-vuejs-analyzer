import time
import random
from typing import Dict, Any, List
import openai

class AI_Agent:
    """A mock AI agent that simulates a call to an AI model for text analysis."""

    def __init__(self, model_name: str, focus: str):
        self.model_name = model_name
        self.focus = focus
        self.client = openai.OpenAI()

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulates a call to an AI model for analysis."""
        content_to_analyze = data.get("content", "")
        
        time.sleep(random.uniform(0.5, 1.5))

        if self.focus == "Risk":
            return self._analyze_risk(content_to_analyze)
        elif self.focus == "Compliance":
            return self._analyze_compliance(content_to_analyze)
        elif self.focus == "Fraud":
            return self._analyze_fraud(content_to_analyze)
        else:
            return {"error": "Unknown focus"}

    def _analyze_risk(self, content: str) -> Dict[str, Any]:
        risk_score = random.uniform(0.1, 0.9)
        findings = []
        if "high-value" in content.lower():
            findings.append("Content mentions 'high-value', indicating potential risk.")
            risk_score = max(risk_score, 0.7)
        if "urgent" in content.lower():
            findings.append("Content mentions 'urgent', which can be a risk factor.")
            risk_score = max(risk_score, 0.6)
        return {
            "model": self.model_name,
            "focus": self.focus,
            "risk_score": risk_score,
            "findings": findings,
        }

    def _analyze_compliance(self, content: str) -> Dict[str, Any]:
        compliance_issues = []
        if "sanction" in content.lower() and "screened" not in content.lower():
            compliance_issues.append("Mention of 'sanction' without confirmation of screening.")
        if "pii" in content.lower() and "encrypted" not in content.lower():
            compliance_issues.append("PII mentioned without confirmation of encryption.")
        return {
            "model": self.model_name,
            "focus": self.focus,
            "compliance_status": "ok" if not compliance_issues else "issues_found",
            "issues": compliance_issues,
        }

    def _analyze_fraud(self, content: str) -> Dict[str, Any]:
        fraud_indicators = []
        if "password" in content.lower() and "reset" in content.lower():
            fraud_indicators.append("Password reset request could be a fraud attempt.")
        if "unusual login" in content.lower():
            fraud_indicators.append("Unusual login activity detected.")
        return {
            "model": self.model_name,
            "focus": self.focus,
            "fraud_probability": random.uniform(0.05, 0.6),
            "indicators": fraud_indicators,
        }

class MultiAgentSystem:
    """Orchestrates analysis from multiple AI agents."""

    def __init__(self):
        self.agents = [
            AI_Agent(model_name="gpt-4.1-mini", focus="Risk"),
            AI_Agent(model_name="gemini-2.5-flash", focus="Compliance"),
            AI_Agent(model_name="gpt-4.1-nano", focus="Fraud"),
        ]

    def analyze_content(self, content: str) -> List[Dict[str, Any]]:
        """Runs a block of content through all agents and aggregates the results."""
        analysis_input = {"content": content}
        results = []
        for agent in self.agents:
            results.append(agent.analyze(analysis_input))
        return results

multi_agent_system = MultiAgentSystem()

