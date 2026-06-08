from __future__ import annotations
import sys
from pathlib import Path

from sandbox import Sandbox
from tool import ToolRegistry
from tools.read_file import ReadFileTool
from tools.list_directory import ListDirectoryTool
from tools.write_file import WriteFileTool
from tools.diff_file import DiffFileTool
from llm import LLM
from agent import run_agent


def _build_registry(sandbox: Sandbox) -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(ReadFileTool(sandbox))
    registry.register(ListDirectoryTool(sandbox))
    registry.register(WriteFileTool(sandbox))
    registry.register(DiffFileTool(sandbox))
    return registry


def _print_tools(registry: ToolRegistry) -> None:
    print("Available tools:")
    for t in registry.list_tools():
        params = t.get_parameters()
        args = ", ".join(
            f"{k}: {v.get('type', '?')}"
            + (" (required)" if v.get("required") else "")
            for k, v in params.items()
        )
        print(f"  {t.get_name()}")
        print(f"    {t.get_description()}")
        if args:
            print(f"    args: {args}")
    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Mini Agent - Local Agent Runtime from scratch with Ollama"
    )
    parser.add_argument("--model", default="qwen3:4b", help="Ollama model name")
    parser.add_argument("--workspace", default="./workspace", help="Sandbox workspace directory")
    parser.add_argument("--list-tools", action="store_true", help="List available tools and exit")
    parser.add_argument("--no-memory", action="store_true", help="Disable conversation memory")
    parser.add_argument("prompt", nargs="*", help="Direct prompt (omit for interactive mode)")
    args = parser.parse_args()

    sandbox = Sandbox(args.workspace)
    Path(args.workspace).mkdir(parents=True, exist_ok=True)

    registry = _build_registry(sandbox)
    if args.list_tools:
        _print_tools(registry)
        return

    llm = LLM(model=args.model)

    if args.prompt:
        prompt = " ".join(args.prompt)
        print(f">>> {prompt}\n")
        answer, _ = run_agent(llm, registry, prompt)
        print(answer)
        return

    messages: list[dict] | None = None if args.no_memory else []
    print(f"Mini Agent (model: {args.model}, workspace: {args.workspace})")
    print(f"Tools: {', '.join(t.get_name() for t in registry.list_tools())}")
    print("Type 'exit' or 'quit' to stop.\n")
    while True:
        try:
            prompt = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if prompt.strip().lower() in ("exit", "quit"):
            break
        if not prompt.strip():
            continue
        answer, messages = run_agent(llm, registry, prompt, messages)
        print(answer)
        print()


if __name__ == "__main__":
    main()
