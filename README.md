# Quote MCP Server — a Personal AI Assistant demo

Demo code for the talk **"Custom MCP Server Architecture for Personal AI
Assistance"** (Pesona AI Summit, July 21). It's the practical companion to
Chapter 7 of *Design Multi-Agent AI Systems Using MCP*.

The whole thing is one small MCP server plus the wiring to use it from an
agentic framework (AI-6) and from three coding agents (Claude Code, Codex,
OpenCode). The point: show how little it takes to build a custom MCP server, and
how the *same* server plugs into every MCP-aware host.

> **Following along?** See **[WALKTHROUGH.md](WALKTHROUGH.md)** for reproducible,
> copy-paste steps. This README is the overview.

## What it does

A curated list of quotes grouped by category lives in [`quotes.json`](quotes.json).
The server in [`quote_server/quote_mcp_server.py`](quote_server/quote_mcp_server.py)
exposes two tools over the STDIO transport:

| Tool | Input | Returns |
| --- | --- | --- |
| `list_categories` | — | The categories that have quotes, comma-separated |
| `get_quote` | `category` | A random quote for that category, or **nothing** when the category is unknown or empty |

It's built on the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
`FastMCP` helper — each tool is just a decorated function. That's the whole
server.

## Layout

```
summit-ai-mcp-demo/
├── quotes.json                     # the curated quotes, by category
├── quote_server/
│   ├── quote_mcp_server.py         # the MCP server (FastMCP)
│   └── try_server.py               # STDIO smoke-test client (no LLM)
├── ai6/
│   ├── config.yaml                 # AI-6 config that points at the server
│   ├── quote_assistant.py          # a tiny AI-6 CLI that uses it
│   └── native_tools/               # (empty) AI-6 native-tools dir
├── .mcp.json                       # Claude Code MCP config (reference)
├── opencode.json                   # OpenCode MCP config (reference)
├── pyproject.toml                  # deps: mcp[cli], ai-six
├── WALKTHROUGH.md                  # step-by-step for attendees
└── README.md
```

## Quick start

```bash
uv sync                                    # install everything into .venv

# 1. Smoke-test the server over STDIO (no API key, no browser):
uv run python try_server.py

# 2. Chat with the AI-6 assistant that uses it (needs OPENAI_API_KEY):
export OPENAI_API_KEY=sk-...
uv run python ai6/quote_assistant.py
```

(Prefer a visual tool? `uv run mcp dev quote_server/quote_mcp_server.py` opens
the MCP Inspector — see [WALKTHROUGH.md](WALKTHROUGH.md#12--optional-the-visual-mcp-inspector)
for the one manual step the current Inspector needs.)

```
👤 [You]: give me a stoic quote
🤖 [Assistant]:
  🔧 [list_categories()] -> creativity, engineering, humor, motivation, stoicism
  🔧 [get_quote(category='stoicism')] -> “Waste no more time arguing about what a good man should be. Be one.” — Marcus Aurelius
“Waste no more time arguing about what a good man should be. Be one.” — Marcus Aurelius
```

## How AI-6 picks it up

[`ai6/config.yaml`](ai6/config.yaml) is a normal AI-6 config. The one line that
brings in our server is `mcp_tools_dirs`:

```yaml
mcp_tools_dirs:
  - ${DEMO_DIR}/quote_server
```

AI-6 scans that directory, launches every MCP server it finds over STDIO,
discovers their tools, and hands them to the agent as if they were native tools.
No glue code — just configuration. AI-6 itself is a PyPI dependency
(`ai-six`), so there's nothing extra to clone.

## Using the server from coding agents

The same server drops into any MCP host. All three launch it the same way — via
`uv`, so it runs inside this repo's virtualenv where `mcp` is installed. Full
steps and verification in [WALKTHROUGH.md](WALKTHROUGH.md#part-3--use-it-from-coding-agents-no-api-key-needed-for-setup); the one-liners:

```bash
# Claude Code (writes .mcp.json)
claude mcp add quotes --scope project \
  -- uv --directory ~/git/summit-ai-mcp-demo run python quote_server/quote_mcp_server.py

# Codex (writes ~/.codex/config.toml)
codex mcp add quotes \
  -- uv --directory ~/git/summit-ai-mcp-demo run python quote_server/quote_mcp_server.py

# OpenCode: edit the path in opencode.json, then `opencode mcp list`
```

## The takeaway

One ~65-line server, written once against the MCP interface, works unchanged in
an agentic framework and in three different coding agents. That's the promise of
MCP: build the tool once, use it everywhere.

## Resources

- 📖 **[Design Multi-Agent AI Systems Using MCP and A2A](https://www.amazon.com/Design-Multi-Agent-Systems-Using-MCP/dp/1806116472)** — Check out Chapter 7
- 📝 **[Claude Code Deep Dive: MCP Unleashed](https://medium.com/@the.gigi/claude-code-deep-dive-mcp-unleashed-0c7692f9c2c2)** — Medium article
- 🔬 **[Making SPACE: Secure and Efficient Runtimes for Long-Running Agents](https://research.perplexity.ai/articles/making-space-secure-and-efficient-runtimes-for-long-running-agents)** — Perplexity research
