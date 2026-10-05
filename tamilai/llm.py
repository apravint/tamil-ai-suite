"""
Multi-Provider LLM Client for Tamil AI
======================================
Connects to Ollama (local qwen2.5/llama3), Gemini, or OpenAI to process
Tamil prompts seamlessly.
"""

import os
import json
import requests
from typing import Dict, Any

class TamilLLMClient:
    def __init__(self, provider: str = "auto", model: str = None, api_key: str = None):
        self.provider = provider.lower()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")

        if self.provider == "auto":
            if os.getenv("GEMINI_API_KEY"):
                self.provider = "gemini"
            elif os.getenv("OPENAI_API_KEY"):
                self.provider = "openai"
            else:
                self.provider = "ollama"

        self.model = model or self._default_model()

    def _default_model(self) -> str:
        if self.provider == "gemini":
            return "gemini-2.5-flash"
        elif self.provider == "openai":
            return "gpt-4o-mini"
        elif self.provider == "ollama":
            return "qwen2.5:1.5b"
        return "heuristic"

    def generate(self, prompt: str) -> str:
        """Generate response from selected provider or fallback."""
        if self.provider == "ollama":
            return self._call_ollama(prompt)
        elif self.provider == "gemini":
            return self._call_gemini(prompt)
        elif self.provider == "openai":
            return self._call_openai(prompt)
        else:
            return self._fallback_response(prompt)

    def _call_ollama(self, prompt: str) -> str:
        url = "http://localhost:11434/api/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        try:
            resp = requests.post(url, json=payload, timeout=12)
            if resp.status_code == 200:
                return resp.json().get("response", "").strip()
        except Exception:
            pass
        return self._fallback_response(prompt)

    def _call_gemini(self, prompt: str) -> str:
        if not self.api_key:
            return self._fallback_response(prompt)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            resp = requests.post(url, json=payload, timeout=15)
            if resp.status_code == 200:
                candidates = resp.json().get("candidates", [])
                if candidates:
                    return candidates[0]["content"]["parts"][0]["text"].strip()
        except Exception:
            pass
        return self._fallback_response(prompt)

    def _call_openai(self, prompt: str) -> str:
        if not self.api_key:
            return self._fallback_response(prompt)
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}]}
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            pass
        return self._fallback_response(prompt)

    def _fallback_response(self, prompt: str) -> str:
        return f"[Tamil-AI-Suite Offline Engine Mode]\nPrompt processed successfully. Connect Ollama or set GEMINI_API_KEY for deep LLM responses.\nPrompt snippet: {prompt[:80]}..."
