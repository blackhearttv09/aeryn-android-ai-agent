from __future__ import annotations

import json
import subprocess
import time
from typing import Any


def run_adb_command(command: str) -> tuple[str, str, int]:
    """Run an adb shell command and return stdout, stderr, exit code."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode


class ADBController:
    """Minimal Android automation layer using ADB commands."""

    def open_app(self, package: str, activity: str | None = None) -> tuple[str, str, int]:
        target = f"{package}/{activity}" if activity else package
        return run_adb_command(f"adb shell am start -n {target}")

    def tap(self, x: int, y: int) -> tuple[str, str, int]:
        return run_adb_command(f"adb shell input tap {x} {y}")

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 200) -> tuple[str, str, int]:
        return run_adb_command(f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}")

    def type_text(self, text: str) -> tuple[str, str, int]:
        safe_text = text.replace("\\", "\\\\").replace('"', '\\"')
        return run_adb_command(f'adb shell input text "{safe_text}"')

    def press_back(self) -> tuple[str, str, int]:
        return run_adb_command("adb shell input keyevent 4")

    def press_home(self) -> tuple[str, str, int]:
        return run_adb_command("adb shell input keyevent 3")

    def wait(self, seconds: float = 1.0) -> None:
        time.sleep(seconds)

    def get_ui_dump(self) -> tuple[str, str, int]:
        return run_adb_command("adb shell uiautomator dump /sdcard/ui.xml")

    def pull_ui_dump(self, out_path: str = "./ui.xml") -> tuple[str, str, int]:
        pull_out, pull_err, pull_code = run_adb_command("adb pull /sdcard/ui.xml " + out_path)
        return pull_out, pull_err, pull_code


class AndroidAutomationRunner:
    def __init__(self, controller: ADBController | None = None):
        self.controller = controller or ADBController()

    def open_settings(self) -> dict[str, Any]:
        stdout, stderr, code = self.controller.open_app("com.android.settings", ".Settings")
        return {"status": "success" if code == 0 else "failed", "stdout": stdout, "stderr": stderr, "code": code}

    def open_app_store(self) -> dict[str, Any]:
        stdout, stderr, code = self.controller.open_app("com.android.vending", ".AssetBrowserActivity")
        return {"status": "success" if code == 0 else "failed", "stdout": stdout, "stderr": stderr, "code": code}

    def safe_example(self) -> dict[str, Any]:
        self.controller.wait(2)
        self.controller.tap(540, 1800)
        self.controller.wait(1)
        return {"status": "ok", "action": "safe_tap_example"}


if __name__ == "__main__":
    runner = AndroidAutomationRunner()
    print("Opening Android settings...")
    print(runner.open_settings())
    time.sleep(3)
    print("Opening app store...")
    print(runner.open_app_store())
