from __future__ import annotations

import uuid
from typing import Any

from aeryn_core.config import AerynConfig
from aeryn_core.llm import GeminiClient, GroqClient
from aeryn_core.memory import LocalMemory, TaskState


class AerynAgent:
    def __init__(self, config: AerynConfig, memory: LocalMemory | None = None):
        self.config = config
        self.memory = memory or LocalMemory(config.db_path)
        self.gemini = GeminiClient(config.gemini_api_key)
        self.groq = GroqClient(config.groq_api_key)

    def create_task(self, goal: str, context: str | None = None) -> TaskState:
        task_id = str(uuid.uuid4())
        task = TaskState(
            task_id=task_id,
            status="queued",
            current_step="ready",
            timeout_seconds=self.config.timeout_seconds,
            metadata={"goal": goal, "context": context or ""},
        )
        task.mark_started()
        self.memory.upsert_task(task)
        self.memory.log_event(task_id, "task_created", {"goal": goal, "context": context or ""})
        return task

    def plan_task(self, goal: str, context: str | None = None) -> dict[str, Any]:
        return self.groq.plan(goal=goal, context=context)

    def respond(self, user_input: str) -> str:
        return self.gemini.ask(
            prompt=user_input,
            system_prompt="You are Aeryn, a universal Android voice AI assistant. Keep answers concise, practical, and permission-aware.",
        )


__all__ = ["AerynAgent"]
