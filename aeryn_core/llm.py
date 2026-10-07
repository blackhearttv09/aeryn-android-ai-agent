from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


@dataclass
class TaskState:
    task_id: str
    status: str = "queued"
    retries: int = 0
    timeout_seconds: int = 120
    started_at: datetime | None = None
    updated_at: datetime | None = None
    last_error: str | None = None
    current_step: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

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

    def can_retry(self, max_retries: int) -> bool:
        return self.retries < max_retries

    def is_timed_out(self) -> bool:
        if self.started_at is None:
            return False
        return datetime.utcnow() - self.started_at > timedelta(seconds=self.timeout_seconds)


class LocalMemory:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_db()

    def _ensure_db(self) -> None:
        path = Path(self.db_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                retries INTEGER DEFAULT 0,
                timeout_seconds INTEGER DEFAULT 120,
                started_at TEXT,
                updated_at TEXT,
                last_error TEXT,
                current_step TEXT,
                metadata TEXT DEFAULT '{}'
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT,
                event_type TEXT NOT NULL,
                payload TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memory (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        conn.close()

    def upsert_task(self, task: TaskState) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            INSERT INTO tasks (task_id, status, retries, timeout_seconds, started_at, updated_at, last_error, current_step, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(task_id) DO UPDATE SET
                status = excluded.status,
                retries = excluded.retries,
                timeout_seconds = excluded.timeout_seconds,
                started_at = excluded.started_at,
                updated_at = excluded.updated_at,
                last_error = excluded.last_error,
                current_step = excluded.current_step,
                metadata = excluded.metadata
            """,
            (
                task.task_id,
                task.status,
                task.retries,
                task.timeout_seconds,
                task.started_at.isoformat() if task.started_at else None,
                task.updated_at.isoformat() if task.updated_at else None,
                task.last_error,
                task.current_step,
                str(task.metadata),
            ),
        )
        conn.commit()
        conn.close()

    def get_task(self, task_id: str) -> TaskState | None:
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT task_id, status, retries, timeout_seconds, started_at, updated_at, last_error, current_step, metadata FROM tasks WHERE task_id = ?",
            (task_id,),
        ).fetchone()
        conn.close()

        if row is None:
            return None

        task_id, status, retries, timeout_seconds, started_at, updated_at, last_error, current_step, metadata = row

        return TaskState(
            task_id=task_id,
            status=status,
            retries=retries,
            timeout_seconds=timeout_seconds,
            started_at=datetime.fromisoformat(started_at) if started_at else None,
            updated_at=datetime.fromisoformat(updated_at) if updated_at else None,
            last_error=last_error,
            current_step=current_step,
            metadata=dict(eval(metadata or '{}')),
        )

    def log_event(self, task_id: str, event_type: str, payload: str | dict | None = None) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO events (task_id, event_type, payload) VALUES (?, ?, ?)",
            (task_id, event_type, str(payload) if payload is not None else None),
        )
        conn.commit()
        conn.close()

    def set_memory(self, key: str, value: str) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO memory (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP",
            (key, value),
        )
        conn.commit()
        conn.close()

    def get_memory(self, key: str) -> str | None:
        conn = sqlite3.connect(self.db_path)
        row = conn.execute("SELECT value FROM memory WHERE key = ?", (key,)).fetchone()
        conn.close()
        return row[0] if row else None


__all__ = ["TaskState", "LocalMemory"]
