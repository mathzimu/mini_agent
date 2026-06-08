from __future__ import annotations
from tool import Tool
from sandbox import Sandbox


class ReadFileTool(Tool):
    def __init__(self, sandbox: Sandbox):
        self._sandbox = sandbox

    def get_name(self) -> str:
        return "read_file"

    def get_description(self) -> str:
        return "Read the content of a file"

    def get_parameters(self) -> dict:
        return {
            "path": {
                "type": "string",
                "description": "Path relative to workspace",
                "required": True,
            }
        }

    def invoke(self, args: dict) -> str:
        path = args.get("path", "")
        if not path:
            return "Error: 'path' argument is required"
        full_path = self._sandbox.resolve(path)
        if not full_path.exists():
            return f"Error: file not found: {path}"
        if not full_path.is_file():
            return f"Error: not a file: {path}"
        return full_path.read_text(encoding="utf-8")
