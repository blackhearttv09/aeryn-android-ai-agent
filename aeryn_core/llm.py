from __future__ import annotations

import json
from typing import Any

import requests


class GeminiClient:
    def __init__(self, api_key: str | None, offline_mode: bool = False):
        self.api_key = api_key
        self.offline_mode = offline_mode

    def ask(self, prompt: str, system_prompt: str | None = None) -> str:
        if self.offline_mode or not self.api_key:
            return self._fallback_response(prompt, system_prompt)

        try:
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "system_instruction": {"parts": [{"text": system_prompt or "You are Aeryn, a helpful Android voice AI agent."}]},
            }

            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key,
            }

            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"
            response = requests.post(url, headers=headers, json=payload, timeout=30, verify=False)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return self._fallback_response(prompt, system_prompt, error=str(e))

    def _fallback_response(self, prompt: str, system_prompt: str | None = None, error: str | None = None) -> str:
        if error:
            return f"[OFFLINE FALLBACK] Gemini API error: {error[:100]}. Processing offline: {prompt[:50]}..."
        return f"[OFFLINE MODE] Response to: {prompt[:60]}...\nSystem: {(system_prompt or 'default')[:40]}..."


class GroqClient:
    def __init__(self, api_key: str | None, offline_mode: bool = False):
        self.api_key = api_key
        self.offline_mode = offline_mode

    def plan(self, goal: str, context: str | None = None) -> dict[str, Any]:
        if self.offline_mode or not self.api_key:
            return self._fallback_plan(goal, context)

        try:
            instructions = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are Aeryn's task planner. Return JSON with 'steps' and 'risks'."},
                    {"role": "user", "content": f"Goal: {goal}\n\nContext:\n{context or 'None'}"},
                ],
                "temperature": 0.2,
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=instructions,
                timeout=30,
                verify=False,
            )
            response.raise_for_status()
            data = response.json()

            content = data["choices"][0]["message"]["content"]
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"raw": content}
        except Exception as e:
            return self._fallback_plan(goal, context, error=str(e))

    def _fallback_plan(self, goal: str, context: str | None = None, error: str | None = None) -> dict[str, Any]:
        return {
            "steps": [
                "Step 1: Observe current screen state",
                "Step 2: Identify UI elements relevant to goal",
                "Step 3: Plan task decomposition",
                "Step 4: Execute actions safely",
                "Step 5: Verify results and recover if needed",
            ],
            "risks": [f"Offline mode active"] + ([f"API Error: {error[:50]}..."] if error else []),
            "goal": goal,
            "context": context or "offline",
        }


__all__ = ["GeminiClient", "GroqClient"]
