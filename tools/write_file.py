from __future__ import annotations
from tool import Tool
from sandbox import Sandbox


class WriteFileTool(Tool):
    def __init__(self, sandbox: Sandbox):
        self._sandbox = sandbox

    def get_name(self) -> str:
        return "write_file"

    def get_description(self) -> str:
        return "Write content to a file (creates or overwrites)"

    def get_parameters(self) -> dict:
        return {
            "path": {
                "type": "string",
                "description": "Path relative to workspace",
                "required": True,
            },
            "content": {
                "type": "string",
                "description": "Content to write",
                "required": True,
            },
        }

    def invoke(self, args: dict) -> str:
        path = args.get("path", "")
        content = args.get("content", "")
        if not path:
            return "Error: 'path' argument is required"
        full_path = self._sandbox.resolve(path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        return f"Successfully wrote {len(content)} bytes to {path}"
