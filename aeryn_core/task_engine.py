from __future__ import annotations

from dataclasses import dataclass
from typing import Any


RISKY_PATTERNS = {
    "payment": ["pay", "payment", "purchase", "checkout", "card", "bank transfer"],
    "message_send": ["send message", "sms", "text message", "whatsapp", "telegram"],
    "call_send": ["call", "dial", "voice call"],
    "account_change": ["account", "security", "password", "2fa", "logout", "login"],
    "destructive": ["delete", "remove", "wipe", "format", "uninstall", "factory reset"],
}


@dataclass
class SafetyDecision:
    risky: bool
    category: str | None
    requires_confirmation: bool
    reason: str


class RiskGuard:
    def __init__(self, require_confirmation: bool = True):
        self.require_confirmation = require_confirmation

    def evaluate(self, action: str, context: str | None = None) -> SafetyDecision:
        normalized = (action + " " + (context or "")).lower()
        for category, patterns in RISKY_PATTERNS.items():
            if any(pattern in normalized for pattern in patterns):
                return SafetyDecision(
                    risky=True,
                    category=category,
                    requires_confirmation=self.require_confirmation,
                    reason=f"Action matches risky category: {category}",
                )
        return SafetyDecision(
            risky=False,
            category=None,
            requires_confirmation=False,
            reason="No risky action pattern detected",
        )

    def confirm(self, action: str, context: str | None = None) -> bool:
        decision = self.evaluate(action, context)
        if not decision.risky:
            return True
        return decision.requires_confirmation


__all__ = ["RiskGuard", "SafetyDecision", "RISKY_PATTERNS"]
