import asyncio
import logging

from mcp import Client, StdioServerParameters

logging.disable(logging.CRITICAL)


async def main():
    params = StdioServerParameters(command="python", args=["agentic_ai/mcp/server.py"])
    async with Client(params) as client:
        tools = await client.list_tools()
        print([t.name for t in tools.tools])

        result = await client.call_tool("get_consumer_lag", {"group": "order-svc"})
        print("ok:", result.structured_content)

        result = await client.call_tool("get_consumer_lag", {"group": "foo"})
        print("tool error:", result.is_error, result.content)


asyncio.run(main())
