from __future__ import annotations
from typing import Any


class Tool:
    def get_name(self) -> str:
        raise NotImplementedError

    def get_description(self) -> str:
        raise NotImplementedError

    def get_parameters(self) -> dict[str, dict]:
        """Return a dict of parameter-name → {type, description, required}."""
        return {}

    def invoke(self, args: dict[str, Any]) -> str:
        raise NotImplementedError


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.get_name()] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())

    def to_tool_specs(self) -> list[dict]:
        return [
            {
                "name": t.get_name(),
                "description": t.get_description(),
                "parameters": t.get_parameters(),
            }
            for t in self._tools.values()
        ]
