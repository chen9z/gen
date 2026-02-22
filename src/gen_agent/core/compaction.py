from __future__ import annotations

from dataclasses import dataclass

from gen_agent.models.messages import (
    AgentMessage,
    AssistantMessage,
    CompactionSummaryMessage,
    UserMessage,
    now_ms,
)


@dataclass
class CompactionDecision:
    should_compact: bool
    reason: str | None
    estimated_tokens: int


def estimate_message_tokens(messages: list[AgentMessage]) -> int:
    chars = 0
    for message in messages:
        if isinstance(message, UserMessage):
            if isinstance(message.content, str):
                chars += len(message.content)
            else:
                chars += sum(len(getattr(block, "text", "")) for block in message.content)
        elif isinstance(message, AssistantMessage):
            chars += sum(len(getattr(block, "text", "") or getattr(block, "thinking", "")) for block in message.content)
        else:
            chars += len(str(message))
    return max(1, chars // 4)


def should_compact(messages: list[AgentMessage], reserve_tokens: int, keep_recent_tokens: int) -> CompactionDecision:
    est = estimate_message_tokens(messages)
    threshold = reserve_tokens + keep_recent_tokens
    if est > threshold:
        return CompactionDecision(True, "threshold", est)
    return CompactionDecision(False, None, est)


def generate_compaction_summary(messages: list[AgentMessage], max_messages: int = 12) -> str:
    selected = messages[:max_messages]
    lines: list[str] = []
    for message in selected:
        role = getattr(message, "role", "unknown")
        if hasattr(message, "content"):
            content = getattr(message, "content")
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                text = " ".join(getattr(block, "text", "") for block in content if getattr(block, "type", "") == "text")
            else:
                text = ""
        else:
            text = ""
        lines.append(f"- {role}: {text[:200]}")
    return "\n".join(lines) if lines else "(empty)"


def build_compaction_message(summary: str, tokens_before: int) -> CompactionSummaryMessage:
    return CompactionSummaryMessage(summary=summary, tokensBefore=tokens_before, timestamp=now_ms())
