from __future__ import annotations
from tool import Tool
from sandbox import Sandbox


class ListDirectoryTool(Tool):
    def __init__(self, sandbox: Sandbox):
        self._sandbox = sandbox

    def get_name(self) -> str:
        return "list_directory"

    def get_description(self) -> str:
        return "List files and directories"

    def get_parameters(self) -> dict:
        return {
            "path": {
                "type": "string",
                "description": "Directory path relative to workspace (default: .)",
                "required": False,
            }
        }

    def invoke(self, args: dict) -> str:
        path = args.get("path", ".")
        full_path = self._sandbox.resolve(path)
        if not full_path.exists():
            return f"Error: path not found: {path}"
        if not full_path.is_dir():
            return f"Error: not a directory: {path}"
        entries = []
        for entry in sorted(full_path.iterdir()):
            suffix = "/" if entry.is_dir() else ""
            entries.append(f"{entry.name}{suffix}")
        return "\n".join(entries) if entries else "(empty)"
