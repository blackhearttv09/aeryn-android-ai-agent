from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


@dataclass
class AerynConfig:
    gemini_api_key: str | None
    groq_api_key: str | None
    log_level: str = "INFO"
    data_dir: str = "./data"
    db_path: str = "./data/aeryn.db"
    timeout_seconds: int = 120
    max_retries: int = 3
    android_package_name: str = "com.aeryn.agent"

    @classmethod
    def from_env(cls) -> "AerynConfig":
        load_dotenv(dotenv_path=Path(".env"), override=False)

        data_dir = os.getenv("AERYN_DATA_DIR", "./data")
        db_path = os.getenv("AERYN_DB_PATH", os.path.join(data_dir, "aeryn.db"))

        return cls(
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            groq_api_key=os.getenv("GROQ_API_KEY"),
            log_level=os.getenv("AERYN_LOG_LEVEL", "INFO"),
            data_dir=data_dir,
            db_path=db_path,
            timeout_seconds=int(os.getenv("AERYN_TIMEOUT_SECONDS", "120")),
            max_retries=int(os.getenv("AERYN_MAX_RETRIES", "3")),
            android_package_name=os.getenv("ANDROID_PACKAGE_NAME", "com.aeryn.agent"),
        )

    def ensure_directories(self) -> None:
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)


__all__ = ["AerynConfig"]
