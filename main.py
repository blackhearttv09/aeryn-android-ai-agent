from __future__ import annotations

from aeryn_core.agent import AerynAgent
from aeryn_core.config import AerynConfig
from aeryn_core.memory import LocalMemory
from aeryn_core.runtime import ExecutionLoop
from aeryn_core.safety import RiskGuard
from aeryn_core.engine import TaskEngine


def main() -> None:
    config = AerynConfig.from_env()
    config.ensure_directories()

    memory = LocalMemory(config.db_path)
    agent = AerynAgent(config=config, memory=memory)
    loop = ExecutionLoop(agent)
    risk_guard = RiskGuard(require_confirmation=True)
    task_engine = TaskEngine(config=config, memory=memory)

    print("\n=== Aeryn Agent Started ===")
    print(f"Version: 0.1.0")
    mode_str = "Offline Mode" if config.offline_mode else "Online Mode"
    print(f"Mode: {mode_str}")
    print()

    sample_goal = "Open the app store and identify a task-management app suitable for Android."
    print(f"[TASK PLANNING] Goal: {sample_goal}")
    plan = loop.run(sample_goal, context="User is on Android and expects safe, generic device interaction.")
    print(f"Plan Status: {plan.get('status')}")
    print()

    risky_check = risk_guard.evaluate("send a WhatsApp message to my boss", "User expects a normal conversation")
    print(f"[SAFETY CHECK] Action: 'send WhatsApp message'")
    print(f"Risky: {risky_check.risky}, Category: {risky_check.category}, Requires Confirmation: {risky_check.requires_confirmation}")
    print()

    execution = task_engine.create_execution(sample_goal, "safe generic mobile workflow")
    print(f"[TASK EXECUTION] Task ID: {execution.task_id}")
    print(f"Status: {execution.status}")
    print(f"Steps: {[step.name for step in execution.steps]}")
    print()

    response = agent.respond("Hello Aeryn, help me operate this Android device safely.")
    print(f"[AGENT RESPONSE]")
    print(response)
    print()
    print("=== Ready for automation ===")


if __name__ == "__main__":
    main()
