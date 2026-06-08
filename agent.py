from __future__ import annotations
import json
import re
import time
from llm import LLM
from tool import ToolRegistry


def _build_system_prompt(registry: ToolRegistry) -> str:
    specs = registry.to_tool_specs()
    lines = []
    for s in specs:
        params = s.get("parameters", {})
        args_desc = ", ".join(
            f"{k}" + (" (required)" if v.get("required") else "")
            for k, v in params.items()
        )
        desc = s["description"]
        if args_desc:
            desc += f" | args: {args_desc}"
        lines.append(f"  - {s['name']}: {desc}")
    tools_desc = "\n".join(lines)
    return (
        "You are a helpful AI assistant with access to these tools:\n"
        f"{tools_desc}\n\n"
        "To call a tool, respond with ONLY this JSON (no extra text):\n"
        '{"tool": "tool_name", "arguments": {"arg": "value"}}\n\n'
        "When you have the final answer, respond in plain text."
    )


def _extract_tool_call(text: str) -> dict | None:
    m = re.search(r'\{"tool"\s*:\s*"', text)
    if not m:
        return None
    start = m.start()
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                chunk = text[start : i + 1]
                try:
                    data = json.loads(chunk)
                except json.JSONDecodeError:
                    return None
                if "tool" in data:
                    data.setdefault("arguments", {})
                    return data
                return None
    return None


def run_agent(
    llm: LLM,
    registry: ToolRegistry,
    user_input: str,
    messages: list[dict] | None = None,
    verbose: bool = False,
) -> tuple[str, list[dict]]:
    if messages is None:
        messages = [
            {"role": "system", "content": _build_system_prompt(registry)},
        ]

    messages.append({"role": "user", "content": user_input})

    for turn in range(10):
        t0 = time.time()
        response = llm.chat(messages)
        elapsed = time.time() - t0
        content = response.get("content", "")

        tool_call = _extract_tool_call(content)
        if tool_call is None:
            messages.append(response)
            if verbose:
                print(f"  [{turn}] LLM {elapsed:.1f}s -> final answer", flush=True)
            return content, messages

        tool_name = tool_call.get("tool", "")
        arguments = tool_call.get("arguments", {})
        if not isinstance(arguments, dict):
            arguments = {}

        tool = registry.get(tool_name)
        if tool is None:
            result = f"Error: unknown tool '{tool_name}'"
        else:
            try:
                result = tool.invoke(arguments)
            except Exception as e:
                result = f"Error executing {tool_name}: {e}"

        if verbose:
            print(
                f"  [{turn}] LLM {elapsed:.1f}s -> {tool_name}({arguments})",
                flush=True,
            )

        messages.append(response)
        messages.append({"role": "user", "content": f"Tool result:\n{result}"})

    return "Agent stopped: maximum iterations reached.", messages
