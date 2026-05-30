#!/usr/bin/env python3
"""Smoke-test the Quote MCP server over STDIO - no LLM, no browser, no Node.

Launches quote_mcp_server.py as a subprocess, speaks MCP to it, and prints the
tool list plus a few sample calls. This is the quickest way to confirm the
server works:

    uv run python try_server.py
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = Path(__file__).resolve().parent / "quote_server" / "quote_mcp_server.py"


async def main() -> None:
    # Launch the server with the same interpreter running this script.
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:", ", ".join(t.name for t in tools.tools))

            cats = await session.call_tool("list_categories", {})
            print("Categories:", cats.content[0].text)

            quote = await session.call_tool("get_quote", {"category": "stoicism"})
            print("A stoic quote:", quote.content[0].text)

            missing = await session.call_tool("get_quote", {"category": "banana"})
            text = missing.content[0].text if missing.content else ""
            print("Unknown category 'banana':", repr(text), "(nothing, as expected)")


if __name__ == "__main__":
    asyncio.run(main())
