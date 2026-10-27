import json

from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

console = Console()


def print_messages(messages: list[dict]) -> None:
    for m in messages:
        role = m["role"]
        if role == "user":
            console.print(Panel(m["content"], title="user", border_style="cyan"))
        elif role == "assistant":
            parts = []
            if m.get("thinking"):
                parts.append(Text(m["thinking"], style="italic dim"))
            for call in m.get("tool_calls") or []:
                fn = call["function"]
                args = json.dumps(fn["arguments"])
                parts.append(Text(f"-> {fn['name']}({args})", style="bold yellow"))
            if m.get("content"):
                parts.append(Markdown(m["content"]))
            console.print(Panel(Group(*parts), title="assistant", border_style="green"))
        elif role == "tool":
            style = "red" if m["content"].startswith("Error") else "magenta"
            console.print(
                Panel(m["content"], title=f"tool: {m['tool_name']}", border_style=style)
            )
