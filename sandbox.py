from pathlib import Path


class Sandbox:
    def __init__(self, workspace_root: str = "./workspace"):
        self._workspace = Path(workspace_root).resolve()

    def resolve(self, path: str) -> Path:
        target = (self._workspace / path).resolve()
        if not str(target).startswith(str(self._workspace)):
            raise PermissionError(
                f"Access denied: {path} is outside workspace ({self._workspace})"
            )
        return target

    @property
    def workspace(self) -> Path:
        return self._workspace
