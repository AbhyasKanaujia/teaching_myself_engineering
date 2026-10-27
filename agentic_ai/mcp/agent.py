import asyncio
import json
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters
from ollama import AsyncClient
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

MODEL = "gpt-oss:120b-cloud"
MAX_STEPS = 10
WRITE_TOOLS = set()  # List of tools that cnanges things
SERVER = Path(__file__).parent / "server.py"

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
            console.print(
                Panel(Group(*parts), title="assistant", border_style="green")
            )
        elif role == "tool":
            style = "red" if m["content"].startswith("Error") else "magenta"
            console.print(
                Panel(m["content"], title=f"tool: {m['tool_name']}", border_style=style)
            )

 
async def run_agent(question: str) -> str:
    llm = AsyncClient()
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    async with Client(params) as client:
        result = await client.list_tools()
        tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.input_schema,
                },
            }
            for t in result.tools
        ]
        messages = [{"role": "user", "content": question}]

        for step in range(MAX_STEPS):
            response = await llm.chat(model=MODEL, messages=messages, tools=tools)

            messages.append(response.message.model_dump())
            if response.message.tool_calls:
                for call in response.message.tool_calls:
                    name = call.function.name
                    args = dict(call.function.arguments)

                    result = await client.call_tool(name=name, arguments=args)

                    text = "".join(c.text for c in result.content if c.type == "text")

                    if result.is_error:
                        text = f"Error: {text}"

                    messages.append(
                        {"role": "tool", "tool_name": name, "content": text}
                    )

            else:
                break

        print_messages(messages)

    return ""


asyncio.run(run_agent("Check consumer lag for orders-svc or something"))
