from __future__ import annotations

from typing import Any

from aeryn_core.agent import AerynAgent
from aeryn_core.config import AerynConfig


class ExecutionLoop:
    def __init__(self, agent: AerynAgent):
        self.agent = agent

    def run(self, user_goal: str, context: str | None = None) -> dict[str, Any]:
        task = self.agent.create_task(user_goal, context)
        try:
            raw_plan = self.agent.plan_task(user_goal, context)
            task.current_step = "planned"
            self.agent.memory.upsert_task(task)

            result = {
                "task_id": task.task_id,
                "status": "success",
                "plan": raw_plan,
                "message": f"Task accepted and planned: {user_goal}",
            }

            task.mark_completed()
            self.agent.memory.upsert_task(task)
            return result
        except Exception as exc:
            task.mark_failed(str(exc))
            self.agent.memory.upsert_task(task)
            return {
                "task_id": task.task_id,
                "status": "failed",
                "error": str(exc),
            }


__all__ = ["ExecutionLoop"]
