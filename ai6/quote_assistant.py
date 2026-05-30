#!/usr/bin/env python3
"""Quote Assistant - a tiny AI-6 CLI wired to our Quote MCP server.

This is a self-contained AI-6 frontend. It loads ``config.yaml`` (which points
AI-6 at our MCP server via ``mcp_tools_dirs``), builds an Agent, and runs an
interactive chat loop. The agent calls the MCP tools on its own when the
conversation calls for a quote.

Run it from this repo's virtualenv (created by ``uv sync``):

    cd ~/git/summit-ai-mcp-demo
    OPENAI_API_KEY=sk-... uv run python ai6/quote_assistant.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Repo root. config.yaml interpolates ${DEMO_DIR}, so the config is portable
# no matter where the repo was cloned.
DEMO_DIR = Path(__file__).resolve().parent.parent
os.environ.setdefault("DEMO_DIR", str(DEMO_DIR))

from ai_six.agent.agent import Agent
from ai_six.agent.config import Config

CONFIG_PATH = DEMO_DIR / "ai6" / "config.yaml"


def handle_chunk(chunk: str) -> None:
    print(chunk, end="", flush=True)


def handle_tool_call(name: str, args: dict, result: str) -> None:
    arg_str = ", ".join(f"{k}={v!r}" for k, v in args.items()) if args else ""
    print(f"\n  🔧 [{name}({arg_str})] -> {result or '(nothing)'}")


def main() -> None:
    load_dotenv()

    config = Config.from_file(str(CONFIG_PATH))
    # The Agent's invariant requires the memory dir to exist.
    Path(config.memory_dir).mkdir(parents=True, exist_ok=True)

    agent = Agent.from_config_file(str(CONFIG_PATH))

    print("💬 Quote Assistant - ask for a quote (e.g. 'cheer me up' or 'a stoic quote').")
    print("   Type 'exit' to quit.\n")

    try:
        while (user_input := input("👤 [You]: ")).lower() != "exit":
            if not user_input.strip():
                continue
            print("🤖 [Assistant]: ", end="", flush=True)
            agent.stream_message(
                user_input,
                agent.default_model_id,
                on_chunk_func=handle_chunk,
                on_tool_call_func=handle_tool_call,
            )
            print("\n" + "-" * 40)
    except (EOFError, KeyboardInterrupt):
        print()
    finally:
        print(f"Session saved with ID: {agent.get_session_id()}")


if __name__ == "__main__":
    main()
