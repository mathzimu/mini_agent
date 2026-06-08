from __future__ import annotations
import difflib
from tool import Tool
from sandbox import Sandbox


class DiffFileTool(Tool):
    def __init__(self, sandbox: Sandbox):
        self._sandbox = sandbox

    def get_name(self) -> str:
        return "diff_file"

    def get_description(self) -> str:
        return "Show diff between current file and proposed content without modifying it"

    def get_parameters(self) -> dict:
        return {
            "path": {
                "type": "string",
                "description": "Path relative to workspace",
                "required": True,
            },
            "new_content": {
                "type": "string",
                "description": "Proposed new content to compare against",
                "required": True,
            },
        }

    def invoke(self, args: dict) -> str:
        path = args.get("path", "")
        new_content = args.get("new_content", "")
        if not path:
            return "Error: 'path' argument is required"
        full_path = self._sandbox.resolve(path)

        if not full_path.exists():
            old_lines = []
            header = f"--- /dev/null\n+++ {path}"
        else:
            old_lines = full_path.read_text(encoding="utf-8").splitlines(keepends=True)
            header = f"--- {path}\n+++ {path}"

        new_lines = new_content.splitlines(keepends=True)
        diff = list(
            difflib.unified_diff(
                old_lines, new_lines,
                fromfile=path if full_path.exists() else "/dev/null",
                tofile=path,
            )
        )
        if not diff:
            return "(no changes)"

        return header + "\n" + "".join(diff)
