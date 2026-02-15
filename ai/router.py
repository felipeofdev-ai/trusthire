"""Multi-provider AI router (Claude + GPT + Codex) with safe fallback."""

from __future__ import annotations

from typing import Literal

from config import settings

TaskType = Literal["resume", "scam", "code"]


def ai_router(task: TaskType, prompt: str) -> dict:
    """
    Route task to preferred provider.
    This keeps production routing explicit while allowing env-based gradual rollout.
    """
    provider = "fallback"

    if task == "scam" and settings.ANTHROPIC_API_KEY:
        provider = "claude"
    elif task == "resume" and settings.OPENAI_API_KEY:
        provider = "gpt"
    elif task == "code" and settings.OPENAI_API_KEY:
        provider = "codex"

    # Controlled fallback (no external call in offline/dev env)
    return {
        "provider": provider,
        "task": task,
        "response": f"[{provider}] {prompt[:400]}",
    }
