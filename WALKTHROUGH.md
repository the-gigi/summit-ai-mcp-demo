# Walkthrough: build and use a custom MCP server

A step-by-step you can follow on your own machine after the talk. By the end
you'll have built a small MCP server and used it from an agentic framework
(AI-6) and from three coding agents (Claude Code, Codex, OpenCode).

Each part stands alone. **Part 1 and Part 3 need no API keys.** Part 2 (the AI-6
assistant) needs an OpenAI API key.

---

## Prerequisites

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** — the package manager used throughout:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- For Part 2 only: an **OpenAI API key** (`export OPENAI_API_KEY=sk-...`).
- For the coding-agent parts: whichever of **Claude Code**, **Codex**, or
  **OpenCode** you already use. Each part is independent — do only the ones you
  care about.

---

## Step 0 — Get the code

```bash
git clone https://github.com/the-gigi/summit-ai-mcp-demo.git
cd summit-ai-mcp-demo
uv sync
```

`uv sync` creates a `.venv` with everything: the MCP SDK, AI-6, and its
dependencies. That's the only install step.

> The repo path is referenced below as `~/git/summit-ai-mcp-demo`. If you cloned
> it elsewhere, substitute your path (or use `$PWD` while you're in the repo).

---

## Part 1 — The MCP server (no API key needed)

The server is [`quote_server/quote_mcp_server.py`](quote_server/quote_mcp_server.py):
~65 lines built on the MCP Python SDK's `FastMCP` helper. It reads
[`quotes.json`](quotes.json) and exposes two tools:

| Tool | Input | Returns |
| --- | --- | --- |
| `list_categories` | — | The categories that have quotes |
| `get_quote` | `category` | A random quote, or nothing if the category is unknown/empty |

### 1.1 — Smoke-test it (recommended)

[`try_server.py`](try_server.py) launches the server
over STDIO, speaks MCP to it, and prints a few sample calls. No LLM, no browser,
no Node — just the `mcp` SDK you already installed:

```bash
uv run python try_server.py
```

```
Tools: list_categories, get_quote
Categories: creativity, engineering, humor, motivation, stoicism
A stoic quote: “We suffer more often in imagination than in reality.” — Seneca
Unknown category 'banana': '' (nothing, as expected)
```

That's a complete, working MCP server. Everything below is just pointing
different hosts at it.

### 1.2 — Optional: the MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is
Anthropic's official tool for poking at servers (needs Node/npx). It has two
modes.

**CLI mode (recommended — no browser, scriptable):**

```bash
# list the tools
npx @modelcontextprotocol/inspector --cli \
  uv run python quote_server/quote_mcp_server.py \
  --method tools/list

# call a tool
npx @modelcontextprotocol/inspector --cli \
  uv run python quote_server/quote_mcp_server.py \
  --method tools/call --tool-name get_quote --tool-arg category=stoicism
```

The second command prints the quote as JSON. (If your npm registry rejects
scoped packages, add `--registry=https://registry.npmjs.org` to `npx`.)

**GUI mode:**

Point the Inspector at our `.mcp.json` (the same file Claude Code uses) and
name the server — it opens with the STDIO transport and command pre-filled:

```bash
npx @modelcontextprotocol/inspector --config .mcp.json --server quotes
```

A browser tab opens with **Transport Type: STDIO**, **Command: `uv`**, and our
arguments already populated. Click **Connect** (top-left) — the status flips to
**Connected** — then open the **Tools** tab, **List Tools**, and run them.

(The committed `.mcp.json` has an absolute `--directory` path. If you cloned the
repo somewhere other than `~/git/summit-ai-mcp-demo`, edit that path first — or
regenerate the file with the Claude Code step in [3.1](#31--claude-code).)

> ⚠️ Don't use `uv run mcp dev quote_server/quote_mcp_server.py` for the GUI: it
> shells out to the Inspector in a way the current build (0.21.2) ignores, so
> the UI falls back to a streamable-HTTP connection to `localhost:5000` and you
> get `ECONNREFUSED`. The `--config`/`--server` form above avoids that. (If you
> ever land in that state, just set Transport to `STDIO`, Command `uv`,
> Arguments `--directory <repo> run python quote_server/quote_mcp_server.py`,
> and Connect.)

If you just want to confirm the server works, the smoke test in 1.1 is simpler
than any of this.

---

## Part 2 — Use it from AI-6 (needs `OPENAI_API_KEY`)

[AI-6](https://github.com/Sayfan-AI/ai-six) is an agentic framework that supports
MCP out of the box. It's already installed (it's a dependency in
`pyproject.toml`), so there's nothing extra to clone.

### 2.1 — How it's wired

The one line that brings in our server is `mcp_tools_dirs` in
[`ai6/config.yaml`](ai6/config.yaml):

```yaml
mcp_tools_dirs:
  - ${DEMO_DIR}/quote_server
```

AI-6 scans that directory, launches every MCP server it finds over STDIO,
discovers their tools, and hands them to the agent as if they were native
tools. No glue code — just configuration.
[`ai6/quote_assistant.py`](ai6/quote_assistant.py) is a ~60-line frontend that
loads the config, builds an `Agent`, and runs a chat loop.

### 2.2 — Run it

```bash
export OPENAI_API_KEY=sk-...
uv run python ai6/quote_assistant.py
```

Then chat:

```
👤 [You]: give me an engineering quote
🤖 [Assistant]:
  🔧 [list_categories()] -> creativity, engineering, humor, motivation, stoicism
  🔧 [get_quote(category='engineering')] -> “Programs must be written for people to read, and only incidentally for machines to execute.” — Harold Abelson
“Programs must be written for people to read, and only incidentally for machines to execute.” — Harold Abelson
```

The agent decided on its own to call `list_categories` and then `get_quote`.
Type `exit` to quit.

> No OpenAI key? AI-6 also supports local [Ollama](https://ollama.com) models.
> Set `default_model_id` in `ai6/config.yaml` to a supported Ollama model and
> drop the `provider_config.openai` block. The model must be both pulled
> (`ollama pull <model>`) **and** known to AI-6 — it looks the context-window
> size up in a fixed table and errors on anything else. Supported ids:
> `qwen2.5-coder:32b`, `qwen3:32b`, `gpt-oss:20b`, `gpt-oss:120b`,
> `deepseek-r1:70b`, `devstral:24b`. (Tool-calling quality varies by model;
> `gpt-oss:20b` is verified to drive the quote tools correctly.)

---

## Part 3 — Use it from coding agents (no API key needed for setup)

The *same* server drops into any MCP host. All three launch it the same way —
via `uv` so it runs inside this repo's virtualenv where `mcp` is installed.
Replace `~/git/summit-ai-mcp-demo` with your actual clone path.

### 3.1 — Claude Code

```bash
claude mcp add quotes --scope project \
  -- uv --directory ~/git/summit-ai-mcp-demo run python quote_server/quote_mcp_server.py
```

This writes a `.mcp.json` in the repo (already committed here as a reference).
Run `claude` in the repo and approve the project server when prompted, then:

```
> give me a quote about creativity
```

Verify anytime with `claude mcp list`.

### 3.2 — Codex

```bash
codex mcp add quotes \
  -- uv --directory ~/git/summit-ai-mcp-demo run python quote_server/quote_mcp_server.py
```

This adds an `[mcp_servers.quotes]` entry to `~/.codex/config.toml`. Verify with
`codex mcp list`, then ask Codex for a quote.

### 3.3 — OpenCode

OpenCode reads a project [`opencode.json`](opencode.json) (already in this repo):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "quotes": {
      "type": "local",
      "command": ["uv", "--directory", "/absolute/path/to/summit-ai-mcp-demo", "run", "python", "quote_server/quote_mcp_server.py"],
      "enabled": true
    }
  }
}
```

Edit the path to your clone, then from the repo:

```bash
opencode mcp list      # should show: ✓ quotes connected
opencode               # ask it for a quote
```

---

## Cleanup

Remove the registrations when you're done experimenting:

```bash
claude mcp remove quotes --scope project   # or just delete .mcp.json
codex mcp remove quotes                    # edits ~/.codex/config.toml
# OpenCode: delete the "quotes" entry from opencode.json
```

---

## The takeaway

One ~65-line server, written once against the MCP interface, works unchanged in
an agentic framework and in three different coding agents. That's the promise of
MCP: build the tool once, use it everywhere.
