from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ScreenNode:
    text: str | None = None
    resource_id: str | None = None
    class_name: str | None = None
    bounds: tuple[int, int, int, int] | None = None
    clickable: bool = False
    scrollable: bool = False
    enabled: bool = True
    children: list["ScreenNode"] = field(default_factory=list)


@dataclass
class ScreenState:
    timestamp: datetime
    app_package: str | None = None
    app_name: str | None = None
    root_activity: str | None = None
    ui_elements: list[ScreenNode] = field(default_factory=list)
    raw_tree: dict[str, Any] | None = None

    @classmethod
    def from_tree(cls, tree: dict[str, Any] | None, app_package: str | None = None) -> "ScreenState":
        ui_elements: list[ScreenNode] = []
        if tree:
            for node in tree.get("children", []):
                ui_elements.append(ScreenNode(
                    text=node.get("text"),
                    resource_id=node.get("resource_id"),
                    class_name=node.get("class_name"),
                    bounds=node.get("bounds"),
                    clickable=bool(node.get("clickable")),
                    scrollable=bool(node.get("scrollable")),
                    enabled=bool(node.get("enabled")),
                ))
        return cls(
            timestamp=datetime.utcnow(),
            app_package=app_package,
            app_name=tree.get("app_name") if tree else None,
            root_activity=tree.get("activity") if tree else None,
            ui_elements=ui_elements,
            raw_tree=tree,
        )

    def detect_app(self) -> str:
        return self.app_package or self.app_name or "unknown_app"


__all__ = ["ScreenNode", "ScreenState"]
