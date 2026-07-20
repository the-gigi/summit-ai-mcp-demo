# Talk agenda — Custom MCP Server Architecture for Personal AI Assistance

Summit.ai, July 21. Companion to chapter 7 of *Design Multi-Agent AI Systems Using MCP*.
Demo repo: this repo. Reproducible steps: [`../WALKTHROUGH.md`](../WALKTHROUGH.md).

**Slot: 40 min talk + 5 min Q&A.** It's a workshop, so the two live demos (§5 build,
§6 integrate) are the protected core — they're the talk. The conceptual sections are
the dials you flex to stay inside 40.

| # | Section | Min | Flex |
|---|---|---|---|
| 1 | Hook & framing | 2 | Fixed-small |
| 2 | The agentic loop | 3 | Dial — one diagram ↔ live trace |
| 3 | What is MCP? | 5 | Dial — biggest lever (essentials ↔ + architecture diagram + raw JSON-RPC) |
| 4 | What makes a good MCP server | 0–2 | Dial — fold into §5 |
| 5 | **Build your own** (LIVE) | 10 | **Protect** — floor ~10; workshop expands here |
| 6 | **Integrate everywhere** (LIVE, climax) | 11 | **Protect** — floor ~10; never cut below |
| 7 | Security & trust | 3 | Dial — 3 bullets ↔ prompt-injection example |
| 8 | Recap | 2 | Fixed-small |
| | buffer / transitions | ~4 | — |
| | **Q&A** (after the recap) | **5** | separate from the 40 |

## Running long? Pull from the dials, in order
1. §4 design → fold into §5 (save ~2)
2. §3 What is MCP → essentials only (save ~2–3)
3. §2 loop → single diagram, no live trace (save ~1)
4. §7 security → three bullets (save ~1)

Don't touch §5/§6 floors. If the room runs long, cut a concept dial — the
climax (§6) is the last thing to sacrifice. Q&A rides in the last 5 min; if the
demos run hot, take questions and let the recap be one slide.

## Section intents
1. **Hook** — "your assistant is only as good as the tools it can reach" → build once, use everywhere.
2. **Agentic loop** — framework → LLM → tool call → local execution → result → LLM. Concrete with AI-6 + a coding agent. Emphasize: tool definitions travel to the LLM in the prompt.
3. **What is MCP** — client/host/server; JSON-RPC data layer vs STDIO/Streamable-HTTP transport; local vs remote. Primitives: **tools** — note resources, prompts, and MCP Apps exist; we focus on tools only and say why.
4. **What makes a good server** — names/descriptions as prompts, structured vs text, errors, statelessness, the "LLM misuses your tool" failure. Reinforce live in §5.
5. **Build your own** (LIVE) — quote server with FastMCP, `quotes.json`, both tools, `try_server.py` + Inspector.
6. **Integrate everywhere** (LIVE, climax) — same unchanged server → AI-6, Claude Code, Codex, OpenCode; run a real prompt in each.
7. **Security & trust** — local servers run with your permissions; third-party supply chain; secrets; prompt injection via tool results.
8. **Recap** — build once / run everywhere; resources; then Q&A.
