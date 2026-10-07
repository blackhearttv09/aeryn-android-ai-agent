from __future__ import annotations

from aeryn_core.agent import AerynAgent
from aeryn_core.config import AerynConfig
from aeryn_core.memory import LocalMemory
from aeryn_core.runtime import ExecutionLoop
from aeryn_core.safety import RiskGuard
from aeryn_core.task_engine import TaskEngine


def main() -> None:
    config = AerynConfig.from_env()
    config.ensure_directories()

    memory = LocalMemory(config.db_path)
    agent = AerynAgent(config=config, memory=memory)
    loop = ExecutionLoop(agent)
    risk_guard = RiskGuard(require_confirmation=True)
    task_engine = TaskEngine(config=config, memory=memory)

    sample_goal = "Open the app store and identify a task-management app suitable for Android."
    plan = loop.run(sample_goal, context="User is on Android and expects safe, generic device interaction.")
    print(plan)

    risky_check = risk_guard.evaluate("send a WhatsApp message to my boss", "User expects a normal conversation")
    print({
        "risky": risky_check.risky,
        "category": risky_check.category,
        "requires_confirmation": risky_check.requires_confirmation,
    })

    execution = task_engine.create_execution(sample_goal, "safe generic mobile workflow")
    print({
        "task_id": execution.task_id,
        "status": execution.status,
        "steps": [step.name for step in execution.steps],
    })

    response = agent.respond("Hello Aeryn, help me operate this Android device safely.")
    print(response)


if __name__ == "__main__":
    main()
