import difflib
import logging

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

logging.disable(logging.CRITICAL)
mcp = MCPServer("lag-demo")


fake = {"order-svc": 1200, "billing-svc": 0}


@mcp.tool()
def get_consumer_lag(group: str) -> str:
    """Returns the consumer lag for a kafka consumer group."""
    if group not in fake:
        possbile_keys = difflib.get_close_matches(group, fake.keys(), n=3)
        if possbile_keys:
            suggestion = f"Did you mean: {', '.join(possbile_keys)}"
        else:
            suggestion = "Try using the get_group_list tool."
        raise ToolError(f"Unknown consumer group: {group}. {suggestion}")
    return f"{group}: lag {fake[group]}"


@mcp.tool()
def get_group_list() -> list[str]:
    return sorted(fake)


if __name__ == "__main__":
    mcp.run()
