# Talk agenda — Custom MCP Server Architecture for Personal AI Assistance

Summit.ai, July 21. Companion to chapter 7 of *Design Multi-Agent AI Systems Using MCP*.
Demo repo: this repo. Reproducible steps: [`../WALKTHROUGH.md`](../WALKTHROUGH.md).

The two live demos (§6 build, §7 integrate) are the protected core — they're the
talk. The conceptual sections are the dials you flex to hit the slot.

| # | Section | 45 min | 60 min | Flex |
|---|---|---|---|---|
| 1 | Hook & framing | 2 | 3 | Fixed-small |
| 2 | The agentic loop | 4 | 6 | Dial — one diagram ↔ live trace |
| 3 | What is MCP? | 5 | 8 | Dial — biggest lever (essentials ↔ + architecture diagram + raw JSON-RPC) |
| 4 | MCP vs CLI | 2 | 3 | Fixed-small (it's a table) |
| 5 | What makes a good MCP server | 0–2 | 5 | Dial — fold into §6 at 45, own beat at 60 |
| 6 | **Build your own** (LIVE) | 10 | 13 | **Protect** — floor ~10; workshop expands here |
| 7 | **Integrate everywhere** (LIVE, climax) | 11 | 13 | **Protect** — floor ~10; never cut below |
| 8 | Security & trust | 3 | 4 | Dial — 3 bullets ↔ prompt-injection example |
| 9 | Recap + Q&A | 3 | 3 | Fixed-small |
| | buffer / transitions | ~5 | ~2 | — |

## How to flex 60 → 45 (pull ~15 min from dials, in order)
1. §5 design → fold into §6 (save 5)
2. §3 What is MCP → essentials only (save 3)
3. §2 loop → single diagram, no live trace (save 2–3)
4. §8 security → three bullets (save 1–2)

Don't touch §6/§7 floors. If the room runs long, cut a concept dial — the
climax (§7) is the last thing to sacrifice.

## Section intents
1. **Hook** — "your assistant is only as good as the tools it can reach" → build once, use everywhere.
2. **Agentic loop** — framework → LLM → tool call → local execution → result → LLM. Concrete with AI-6 + a coding agent.
3. **What is MCP** — client/host/server; JSON-RPC data layer vs STDIO/Streamable-HTTP transport; local vs remote. Primitives: **tools** — note resources, prompts, and MCP Apps exist; we focus on tools only and say why.
4. **MCP vs CLI** — trade-offs table; when not to bother.
5. **What makes a good server** — names/descriptions as prompts, structured vs text, errors, statelessness, the "LLM misuses your tool" failure. Reinforce live in §6.
6. **Build your own** (LIVE) — quote server with FastMCP, `quotes.json`, both tools, `try_server.py` + Inspector.
7. **Integrate everywhere** (LIVE, climax) — same unchanged server → AI-6, Claude Code, Codex, OpenCode; run a real prompt in each.
8. **Security & trust** — local servers run with your permissions; third-party supply chain; secrets; prompt injection via tool results.
9. **Recap** — build once / run everywhere; resources; Q&A.
