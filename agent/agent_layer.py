# agent_layer.py

from dataclasses import dataclass
from datetime import datetime
import json
import os


HIGH_RISK_KEYWORDS = [
    "execute", "open trade", "close trade", "buy", "sell",
    "leverage", "position size", "risk", "stop loss",
    "take profit", "live", "api key", "kill switch"
]

BLOCKED_INTENTS = [
    "EXECUTION",
    "API_KEYS",
    "RISK_OVERRIDE",
    "KILL_SWITCH_DISABLE"
]


@dataclass
class AgentRequest:
    source: str
    message: str
    requested_action: str


class FalconXAgentLayer:
    def __init__(self, log_path="logs/agent_activity.log"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def classify_intent(self, request: AgentRequest):
        text = f"{request.message} {request.requested_action}".lower()

        if any(word in text for word in ["buy", "sell", "open trade", "close trade", "execute"]):
            return "EXECUTION"

        if any(word in text for word in ["api key", "secret", "passphrase"]):
            return "API_KEYS"

        if any(word in text for word in ["increase risk", "change leverage", "disable kill switch"]):
            return "RISK_OVERRIDE"

        if any(word in text for word in ["analyze", "review", "report", "inspect", "explain"]):
            return "ANALYSIS"

        if any(word in text for word in ["suggest", "improve", "optimize"]):
            return "PROPOSAL"

        return "UNKNOWN"

    def risk_check(self, request: AgentRequest, intent: str):
        text = f"{request.message} {request.requested_action}".lower()

        if intent in BLOCKED_INTENTS:
            return "HIGH"

        if any(keyword in text for keyword in HIGH_RISK_KEYWORDS):
            return "HIGH"

        if intent in ["PROPOSAL"]:
            return "MEDIUM"

        return "LOW"

    def decide(self, intent: str, risk_level: str, human_approval=False):
        if intent in BLOCKED_INTENTS:
            return "BLOCK"

        if risk_level == "HIGH" and not human_approval:
            return "REVIEW"

        if risk_level == "MEDIUM" and not human_approval:
            return "REVIEW"

        return "ALLOW"

    def log_agent_activity(self, request, intent, risk_level, decision):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": request.source,
            "message": request.message,
            "requested_action": request.requested_action,
            "intent": intent,
            "risk_level": risk_level,
            "decision": decision
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def evaluate(self, source, message, requested_action, human_approval=False):
        request = AgentRequest(
            source=source,
            message=message,
            requested_action=requested_action
        )

        intent = self.classify_intent(request)
        risk_level = self.risk_check(request, intent)
        decision = self.decide(intent, risk_level, human_approval)
        self.log_agent_activity(request, intent, risk_level, decision)

        return {
            "intent": intent,
            "risk_level": risk_level,
            "decision": decision
        }
