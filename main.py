from __future__ import annotations

from aeryn_core.agent import AerynAgent
from aeryn_core.config import AerynConfig
from aeryn_core.memory import LocalMemory
from aeryn_core.runtime import ExecutionLoop


def main() -> None:
    config = AerynConfig.from_env()
    config.ensure_directories()

    memory = LocalMemory(config.db_path)
    agent = AerynAgent(config=config, memory=memory)
    loop = ExecutionLoop(agent)

    sample_goal = "Open the app store and identify a task-management app suitable for Android."
    result = loop.run(sample_goal, context="User is on Android and expects safe, generic device interaction.")
    print(result)

    response = agent.respond("Hello Aeryn, help me operate this Android device safely.")
    print(response)


if __name__ == "__main__":
    main()
