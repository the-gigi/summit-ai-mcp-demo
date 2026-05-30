"""Quote MCP server.

A minimal Model Context Protocol server for the talk
"Custom MCP Server Architecture for Personal AI Assistance".

It exposes two tools over the STDIO transport:

* ``list_categories`` - return the categories that have quotes.
* ``get_quote``       - return a random quote for a category, or nothing
                        when the category is unknown or has no quotes.

The quotes live in ``quotes.json`` next to the repo root. Override the
location with the ``QUOTES_FILE`` environment variable if you want to point
the server at a different curated list.
"""

import json
import os
import random
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# quotes.json sits at the repo root, one level up from this file.
DEFAULT_QUOTES_FILE = Path(__file__).resolve().parent.parent / "quotes.json"
QUOTES_FILE = Path(os.environ.get("QUOTES_FILE", DEFAULT_QUOTES_FILE))

# log_level WARNING keeps the per-request INFO chatter off stderr, so host
# output (Inspector, coding agents, our smoke test) stays clean.
mcp = FastMCP("Quotes", log_level="WARNING")


def _load_quotes() -> dict[str, list[dict]]:
    """Load the curated quotes from disk on every call.

    Reading per call keeps the demo simple and lets you edit quotes.json
    while the server is running - handy when presenting live.
    """
    with open(QUOTES_FILE) as f:
        return json.load(f)


@mcp.tool()
def list_categories() -> str:
    """List the categories that have at least one quote, comma-separated."""
    quotes = _load_quotes()
    return ", ".join(sorted(quotes.keys()))


@mcp.tool()
def get_quote(category: str) -> str:
    """Return a random quote for the given category.

    Returns an empty string when the category is unknown or has no quotes,
    so the assistant can tell the user nothing was found.
    """
    quotes = _load_quotes()
    entries = quotes.get(category.strip().lower(), [])
    if not entries:
        return ""
    chosen = random.choice(entries)
    return f"“{chosen['text']}” — {chosen['author']}"


if __name__ == "__main__":
    mcp.run()
