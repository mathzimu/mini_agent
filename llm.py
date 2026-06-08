from __future__ import annotations
import requests


OLLAMA_BASE = "http://localhost:11434"


class LLM:
    def __init__(
        self,
        model: str = "qwen3:4b",
        num_ctx: int = 4096,
        keep_alive: str = "5m",
    ):
        self._model = model
        self._num_ctx = num_ctx
        self._keep_alive = keep_alive
        self._api_url = f"{OLLAMA_BASE}/api/chat"
        self._session = requests.Session()
        self._session.trust_env = False

    def chat(self, messages: list[dict]) -> dict:
        body = {
            "model": self._model,
            "messages": messages,
            "stream": False,
            "keep_alive": self._keep_alive,
            "options": {
                "num_ctx": self._num_ctx,
            },
        }
        resp = self._session.post(self._api_url, json=body, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        msg = data["message"]
        return {
            "role": msg.get("role", "assistant"),
            "content": msg.get("content", ""),
        }

    @property
    def model(self) -> str:
        return self._model
