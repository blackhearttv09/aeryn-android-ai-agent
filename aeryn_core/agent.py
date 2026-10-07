from __future__ import annotations

from typing import Any

import requests


class GeminiClient:
    def __init__(self, api_key: str | None):
        self.api_key = api_key

    def ask(self, prompt: str, system_prompt: str | None = None) -> str:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is missing")

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "system_instruction": {"parts": [{"text": system_prompt or "You are Aeryn, a helpful Android voice AI agent."}]},
        }

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        }

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError):
            raise RuntimeError(f"Unexpected Gemini response: {data}")


class GroqClient:
    def __init__(self, api_key: str | None):
        self.api_key = api_key

    def plan(self, goal: str, context: str | None = None) -> dict[str, Any]:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing")

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

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=instructions, timeout=60)
        response.raise_for_status()
        data = response.json()

        try:
            content = data["choices"][0]["message"]["content"]
            return {"raw": content}
        except (KeyError, IndexError, TypeError):
            raise RuntimeError(f"Unexpected Groq response: {data}")


__all__ = ["GeminiClient", "GroqClient"]
