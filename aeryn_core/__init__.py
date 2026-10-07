from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from aeryn_core.config import AerynConfig
from aeryn_core.memory import LocalMemory, TaskState


@dataclass
class TaskStep:
    name: str
    intent: str
    expected_result: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskExecution:
    task_id: str
    goal: str
    context: str | None = None
    steps: list[TaskStep] = field(default_factory=list)
    status: str = "queued"
    retries: int = 0
    started_at: datetime | None = None
    updated_at: datetime | None = None
    timeout_seconds: int = 120
    last_error: str | None = None

    def mark_started(self) -> None:
        self.started_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.status = "running"

    def mark_failed(self, error: str) -> None:
        self.last_error = error
        self.updated_at = datetime.utcnow()
        self.status = "failed"

    def mark_completed(self) -> None:
        self.updated_at = datetime.utcnow()
        self.status = "completed"

    def is_timed_out(self) -> bool:
        if self.started_at is None:
            return False
        return datetime.utcnow() - self.started_at > timedelta(seconds=self.timeout_seconds)


class TaskEngine:
    def __init__(self, config: AerynConfig, memory: LocalMemory | None = None):
        self.config = config
        self.memory = memory or LocalMemory(config.db_path)

    def build_plan(self, goal: str, context: str | None = None) -> list[TaskStep]:
        base = [
            TaskStep("observe", "Inspect current screen and app state", "The active app and target screen are identified"),
            TaskStep("understand", "Map visible UI to likely action targets", "Relevant controls and text are recognized"),
            TaskStep("plan", "Break the task into safe, ordered steps", "Sub-actions are sequenced with fallback options"),
            TaskStep("control", "Execute the required pointer or accessibility actions", "The action matches the target UI"),
            TaskStep("verify", "Confirm expected state or result", "The objective is achieved or a failure is detected"),
            TaskStep("recover", "If needed, try alternate actions or stop safely", "The system handles failure without looping indefinitely"),
        ]
        for step in base:
            step.metadata["goal"] = goal
            step.metadata["context"] = context or ""
        return base

    def create_execution(self, goal: str, context: str | None = None) -> TaskExecution:
        exec_id = str(uuid.uuid4())
        execution = TaskExecution(
            task_id=exec_id,
            goal=goal,
            context=context,
            steps=self.build_plan(goal, context),
            timeout_seconds=self.config.timeout_seconds,
        )
        execution.mark_started()
        self.memory.upsert_task(TaskState(
            task_id=exec_id,
            status="running",
            current_step="observe",
            timeout_seconds=self.config.timeout_seconds,
            metadata={"goal": goal, "context": context or "", "steps": [step.name for step in execution.steps]},
        ))
        return execution

    def finalize(self, execution: TaskExecution, status: str, error: str | None = None) -> None:
        if status == "completed":
            execution.mark_completed()
        else:
            execution.mark_failed(error or "unknown failure")
        self.memory.upsert_task(TaskState(
            task_id=execution.task_id,
            status=execution.status,
            current_step="completed" if execution.status == "completed" else "failed",
            timeout_seconds=execution.timeout_seconds,
            metadata={"goal": execution.goal, "context": execution.context or "", "steps": [step.name for step in execution.steps]},
            last_error=execution.last_error,
        ))


__all__ = ["TaskStep", "TaskExecution", "TaskEngine"]
