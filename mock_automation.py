from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from typing import Any
from enum import Enum


class ActionType(Enum):
    """Types of automation actions."""
    OPEN_APP = "open_app"
    TAP = "tap"
    SWIPE = "swipe"
    TYPE_TEXT = "type_text"
    PRESS_KEY = "press_key"
    WAIT = "wait"
    SCREENSHOT = "screenshot"
    VERIFY = "verify"


@dataclass
class AutomationAction:
    """Single automation action."""
    action_type: ActionType
    params: dict[str, Any]
    timestamp: float = None
    result: str = "pending"
    error: str | None = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_type": self.action_type.value,
            "params": self.params,
            "timestamp": self.timestamp,
            "result": self.result,
            "error": self.error,
        }


@dataclass
class ExecutionPlan:
    """Complete execution plan with actions."""
    goal: str
    actions: list[AutomationAction]
    safety_level: str = "safe"
    requires_confirmation: bool = False
    created_at: float = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

    def to_dict(self) -> dict[str, Any]:
        return {
            "goal": self.goal,
            "actions": [a.to_dict() for a in self.actions],
            "safety_level": self.safety_level,
            "requires_confirmation": self.requires_confirmation,
            "created_at": self.created_at,
        }


class MockAutomationEngine:
    """Mock Android automation engine for testing without a real device."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.execution_history: list[ExecutionPlan] = []
        self.last_screenshot_path: str | None = None

    def log(self, msg: str) -> None:
        if self.verbose:
            print(f"[MOCK_AUTOMATION] {msg}")

    def open_app(self, package: str, activity: str | None = None) -> AutomationAction:
        """Mock: open an app."""
        target = f"{package}/{activity}" if activity else package
        self.log(f"Opening app: {target}")
        action = AutomationAction(
            action_type=ActionType.OPEN_APP,
            params={"package": package, "activity": activity},
            result="success",
        )
        time.sleep(0.5)
        return action

    def tap(self, x: int, y: int) -> AutomationAction:
        """Mock: tap at coordinates."""
        self.log(f"Tapping at ({x}, {y})")
        action = AutomationAction(
            action_type=ActionType.TAP,
            params={"x": x, "y": y},
            result="success",
        )
        time.sleep(0.2)
        return action

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 500) -> AutomationAction:
        """Mock: swipe action."""
        self.log(f"Swiping from ({x1}, {y1}) to ({x2}, {y2})")
        action = AutomationAction(
            action_type=ActionType.SWIPE,
            params={"x1": x1, "y1": y1, "x2": x2, "y2": y2, "duration": duration},
            result="success",
        )
        time.sleep(0.3)
        return action

    def type_text(self, text: str) -> AutomationAction:
        """Mock: type text."""
        self.log(f"Typing text: {text[:30]}...")
        action = AutomationAction(
            action_type=ActionType.TYPE_TEXT,
            params={"text": text},
            result="success",
        )
        time.sleep(0.2)
        return action

    def press_key(self, key: str) -> AutomationAction:
        """Mock: press a key (back, home, etc)."""
        self.log(f"Pressing key: {key}")
        action = AutomationAction(
            action_type=ActionType.PRESS_KEY,
            params={"key": key},
            result="success",
        )
        time.sleep(0.1)
        return action

    def wait(self, seconds: float) -> AutomationAction:
        """Mock: wait for specified time."""
        self.log(f"Waiting {seconds}s...")
        time.sleep(seconds)
        action = AutomationAction(
            action_type=ActionType.WAIT,
            params={"seconds": seconds},
            result="success",
        )
        return action

    def screenshot(self) -> AutomationAction:
        """Mock: take a screenshot."""
        self.log("Taking screenshot...")
        path = f"./data/screenshot_{int(time.time())}.png"
        self.last_screenshot_path = path
        action = AutomationAction(
            action_type=ActionType.SCREENSHOT,
            params={"path": path},
            result="success",
        )
        return action

    def verify_app_open(self, package: str) -> AutomationAction:
        """Mock: verify an app is open."""
        self.log(f"Verifying app open: {package}")
        action = AutomationAction(
            action_type=ActionType.VERIFY,
            params={"package": package, "check": "app_open"},
            result="verified",
        )
        return action

    def plan_open_settings(self) -> ExecutionPlan:
        """Plan: open Android settings."""
        actions = [
            self.open_app("com.android.settings", ".Settings"),
            self.wait(2.0),
            self.screenshot(),
            self.verify_app_open("com.android.settings"),
        ]
        plan = ExecutionPlan(
            goal="Open Android Settings",
            actions=actions,
            safety_level="safe",
            requires_confirmation=False,
        )
        self.execution_history.append(plan)
        return plan

    def plan_open_play_store(self) -> ExecutionPlan:
        """Plan: open Google Play Store."""
        actions = [
            self.open_app("com.android.vending"),
            self.wait(2.0),
            self.screenshot(),
            self.verify_app_open("com.android.vending"),
        ]
        plan = ExecutionPlan(
            goal="Open Google Play Store",
            actions=actions,
            safety_level="safe",
            requires_confirmation=False,
        )
        self.execution_history.append(plan)
        return plan

    def plan_search_play_store(self, query: str) -> ExecutionPlan:
        """Plan: search in Play Store."""
        actions = [
            self.open_app("com.android.vending"),
            self.wait(1.5),
            self.tap(540, 200),  # tap search box
            self.wait(0.5),
            self.type_text(query),
            self.wait(0.5),
            self.press_key("enter"),
            self.wait(2.0),
            self.screenshot(),
        ]
        plan = ExecutionPlan(
            goal=f"Search Play Store for '{query}'",
            actions=actions,
            safety_level="safe",
            requires_confirmation=False,
        )
        self.execution_history.append(plan)
        return plan

    def plan_send_message(self, contact: str, message: str) -> ExecutionPlan:
        """Plan: send a message (RISKY - requires confirmation)."""
        actions = [
            self.open_app("com.whatsapp"),
            self.wait(1.5),
            self.tap(540, 900),  # tap search/chat
            self.type_text(contact),
            self.wait(1.0),
            self.tap(540, 1000),  # select contact
            self.wait(1.0),
            self.tap(540, 2000),  # tap message box
            self.type_text(message),
            self.tap(900, 2000),  # tap send
            self.wait(1.0),
        ]
        plan = ExecutionPlan(
            goal=f"Send message to {contact}",
            actions=actions,
            safety_level="risky",
            requires_confirmation=True,  # MUST confirm before executing
        )
        self.execution_history.append(plan)
        return plan

    def execute_plan(self, plan: ExecutionPlan, confirm: bool = False) -> dict[str, Any]:
        """Execute an automation plan."""
        if plan.requires_confirmation and not confirm:
            return {
                "status": "blocked",
                "reason": "Plan requires confirmation",
                "plan": plan.to_dict(),
            }

        self.log(f"Executing plan: {plan.goal}")
        for i, action in enumerate(plan.actions):
            self.log(f"  [{i+1}/{len(plan.actions)}] {action.action_type.value}")

        return {
            "status": "completed",
            "goal": plan.goal,
            "actions_executed": len(plan.actions),
            "plan": plan.to_dict(),
        }

    def get_execution_history(self) -> list[dict[str, Any]]:
        """Get all execution history."""
        return [p.to_dict() for p in self.execution_history]


def demo_mock_automation():
    """Demonstrate mock automation engine."""
    engine = MockAutomationEngine(verbose=True)

    print("\n=== Mock Android Automation Engine ===\n")

    # Demo 1: Open Settings
    print("[DEMO 1] Opening Settings...")
    plan = engine.plan_open_settings()
    result = engine.execute_plan(plan)
    print(f"Result: {result['status']}\n")

    # Demo 2: Open Play Store
    print("[DEMO 2] Opening Play Store...")
    plan = engine.plan_open_play_store()
    result = engine.execute_plan(plan)
    print(f"Result: {result['status']}\n")

    # Demo 3: Search Play Store
    print("[DEMO 3] Searching Play Store for 'task manager'...")
    plan = engine.plan_search_play_store("task manager")
    result = engine.execute_plan(plan)
    print(f"Result: {result['status']}\n")

    # Demo 4: Risky action (send message) - blocked without confirmation
    print("[DEMO 4] Attempting to send WhatsApp message (risky)...")
    plan = engine.plan_send_message("Mom", "Hello! I'm using Aeryn.")
    result = engine.execute_plan(plan, confirm=False)
    print(f"Result: {result['status']} - {result['reason']}\n")

    # Demo 5: Risky action WITH confirmation
    print("[DEMO 5] Sending message WITH confirmation...")
    result = engine.execute_plan(plan, confirm=True)
    print(f"Result: {result['status']}\n")

    # Summary
    print(f"\n=== Execution Summary ===")
    print(f"Total plans executed: {len(engine.execution_history)}")
    print(f"Last screenshot: {engine.last_screenshot_path}")


if __name__ == "__main__":
    demo_mock_automation()
