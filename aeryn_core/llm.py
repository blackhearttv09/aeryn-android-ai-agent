from __future__ import annotations

import json
from typing import Any

import requests


class GeminiClient:
    def __init__(self, api_key: str | None):
        self.api_key = api_key

    def ask(self, prompt: str, system_prompt: str | None = None) -> str:
        if not self.api_key:
            return f"[OFFLINE MOCK] Gemini response to: {prompt}\nSystem: {system_prompt or 'default'}"

        try:
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "system_instruction": {"parts": [{"text": system_prompt or "You are Aeryn, a helpful Android voice AI agent."}]},
            }

            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key,
            }

            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"[OFFLINE FALLBACK] Error calling Gemini: {str(e)}. Returning mock response for: {prompt}"


class GroqClient:
    def __init__(self, api_key: str | None):
        self.api_key = api_key

    def plan(self, goal: str, context: str | None = None) -> dict[str, Any]:
        if not self.api_key:
            return {
                "steps": [
                    "Step 1: Observe current screen state",
                    "Step 2: Identify UI elements relevant to goal",
                    "Step 3: Plan task decomposition",
                    "Step 4: Execute actions",
                    "Step 5: Verify results",
                ],
                "risks": ["No API key - using mock planning"],
                "goal": goal,
                "context": context or "offline",
            }

        try:
            instructions = {
                "model": "llama-3.1-70b-versatile",
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

            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=instructions, timeout=10)
            response.raise_for_status()
            data = response.json()

            content = data["choices"][0]["message"]["content"]
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"raw": content}
        except Exception as e:
            return {
                "steps": [
                    "Step 1: Observe current screen state",
                    "Step 2: Identify UI elements relevant to goal",
                    "Step 3: Plan task decomposition",
                    "Step 4: Execute actions",
                    "Step 5: Verify results",
                ],
                "risks": [f"API Error: {str(e)} - using fallback planning"],
                "goal": goal,
                "context": context or "offline",
            }


__all__ = ["GeminiClient", "GroqClient"]
