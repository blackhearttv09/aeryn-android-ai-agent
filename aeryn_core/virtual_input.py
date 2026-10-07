from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ActionType(str, Enum):
    TAP = "tap"
    DOUBLE_TAP = "double_tap"
    LONG_PRESS = "long_press"
    SWIPE = "swipe"
    DRAG = "drag"
    SCROLL = "scroll"
    TYPE_TEXT = "type_text"
    KEY_BACK = "key_back"
    KEY_HOME = "key_home"
    KEY_RECENT = "key_recent"


@dataclass
class PointerAction:
    action: ActionType
    x: int | None = None
    y: int | None = None
    dx: int | None = None
    dy: int | None = None
    text: str | None = None
    duration_ms: int = 200

    def to_dict(self) -> dict[str, Any]:
        data = {"action": self.action.value}
        if self.x is not None:
            data["x"] = self.x
        if self.y is not None:
            data["y"] = self.y
        if self.dx is not None:
            data["dx"] = self.dx
        if self.dy is not None:
            data["dy"] = self.dy
        if self.text is not None:
            data["text"] = self.text
        data["duration_ms"] = self.duration_ms
        return data


class VirtualMouse:
    def __init__(self, overlay_enabled: bool = True):
        self.overlay_enabled = overlay_enabled
        self.x = 0
        self.y = 0

    def move_to(self, x: int, y: int) -> PointerAction:
        self.x = x
        self.y = y
        return PointerAction(action=ActionType.TAP, x=x, y=y)

    def tap(self, x: int, y: int, duration_ms: int = 120) -> PointerAction:
        return PointerAction(action=ActionType.TAP, x=x, y=y, duration_ms=duration_ms)

    def double_tap(self, x: int, y: int, duration_ms: int = 120) -> PointerAction:
        return PointerAction(action=ActionType.DOUBLE_TAP, x=x, y=y, duration_ms=duration_ms)

    def long_press(self, x: int, y: int, duration_ms: int = 800) -> PointerAction:
        return PointerAction(action=ActionType.LONG_PRESS, x=x, y=y, duration_ms=duration_ms)

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 400) -> PointerAction:
        return PointerAction(action=ActionType.SWIPE, x=x1, y=y1, dx=x2 - x1, dy=y2 - y1, duration_ms=duration_ms)

    def drag(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 600) -> PointerAction:
        return PointerAction(action=ActionType.DRAG, x=x1, y=y1, dx=x2 - x1, dy=y2 - y1, duration_ms=duration_ms)

    def scroll(self, direction: str = "down", amount: int = 200) -> PointerAction:
        if direction == "up":
            return PointerAction(action=ActionType.SCROLL, dy=-amount)
        return PointerAction(action=ActionType.SCROLL, dy=amount)

    def type_text(self, text: str) -> PointerAction:
        return PointerAction(action=ActionType.TYPE_TEXT, text=text)

    def back(self) -> PointerAction:
        return PointerAction(action=ActionType.KEY_BACK)

    def home(self) -> PointerAction:
        return PointerAction(action=ActionType.KEY_HOME)

    def recent(self) -> PointerAction:
        return PointerAction(action=ActionType.KEY_RECENT)


__all__ = ["ActionType", "PointerAction", "VirtualMouse"]
