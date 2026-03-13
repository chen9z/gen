# tests/unit/test_stream_view.py
from __future__ import annotations

from rich.console import Console
from rich.text import Text

from gen_agent.interactive.stream_view import StreamView, ToolStatus, _summarize_args
from gen_agent.models.events import (
    AgentStart,
    AgentEnd,
    AutoCompactionEnd,
    AutoCompactionStart,
    AssistantMessageEvent,
    MessageUpdate,
    ToolExecutionEnd,
    ToolExecutionStart,
)
from gen_agent.models.messages import AssistantMessage
from gen_agent.models.content import TextContent


def _assistant_message(text: str = "") -> AssistantMessage:
    return AssistantMessage(
        provider="openai",
        model="gpt-4o-mini",
        content=[TextContent(text=text)] if text else [],
        stopReason="stop",
    )


class _FakeLive:
    """Replaces Rich.Live for testing."""

    def __init__(self):
        self.updates: list = []
        self.started = False
        self.stopped = False

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True

    def update(self, renderable, refresh=True):
        self.updates.append(renderable)


def _make_view() -> tuple[StreamView, _FakeLive]:
    console = Console(file=None, force_terminal=True)
    view = StreamView(console)
    fake = _FakeLive()
    view._live = fake
    return view, fake


def test_stream_view_start_stop():
    view, fake = _make_view()
    view.start()
    assert fake.started
    view.stop()
    assert fake.stopped


def test_stream_view_text_delta_accumulates():
    view, fake = _make_view()
    msg = _assistant_message()

    view.on_event(AgentStart())
    view.on_event(MessageUpdate(
        message=msg,
        assistantMessageEvent=AssistantMessageEvent(type="text_delta", delta="hello "),
    ))
    view.on_event(MessageUpdate(
        message=msg,
        assistantMessageEvent=AssistantMessageEvent(type="text_delta", delta="world"),
    ))

    assert "".join(view._text_parts) == "hello world"
    assert len(fake.updates) >= 2


def test_stream_view_tool_execution_lifecycle():
    view, _ = _make_view()

    view.on_event(AgentStart())
    view.on_event(ToolExecutionStart(
        toolCallId="tc1",
        toolName="read_file",
        args={"path": "src/main.py"},
    ))

    assert "tc1" in view._tools
    assert view._tools["tc1"].name == "read_file"
    assert view._tools["tc1"].status == "running"

    view.on_event(ToolExecutionEnd(
        toolCallId="tc1",
        toolName="read_file",
        result="file content",
        isError=False,
    ))

    assert view._tools["tc1"].status == "done"
    assert view._tools["tc1"].duration > 0
    assert view._tools["tc1"].is_error is False


def test_stream_view_tool_error():
    view, _ = _make_view()
    view.on_event(AgentStart())
    view.on_event(ToolExecutionStart(
        toolCallId="tc2",
        toolName="bash",
        args={"command": "ls"},
    ))
    view.on_event(ToolExecutionEnd(
        toolCallId="tc2",
        toolName="bash",
        result=None,
        isError=True,
        errorDetail="command failed",
    ))

    assert view._tools["tc2"].status == "error"
    assert view._tools["tc2"].is_error is True


def test_stream_view_agent_start_clears_state():
    view, _ = _make_view()
    view._text_parts = ["old text"]
    view._tools["old"] = ToolStatus(name="old_tool")

    view.on_event(AgentStart())

    assert view._text_parts == []
    assert view._tools == {}
    assert view._working is True


def test_stream_view_agent_end_stops_working():
    view, _ = _make_view()
    view.on_event(AgentStart())
    assert view._working is True

    view.on_event(AgentEnd(messages=[]))
    assert view._working is False


def test_stream_view_compaction_notice():
    view, _ = _make_view()
    view.on_event(AutoCompactionStart(reason="threshold"))
    assert view._notice == "Compacting context..."

    view.on_event(AutoCompactionEnd())
    assert view._notice is None


def test_stream_view_error_event():
    view, _ = _make_view()
    msg = _assistant_message()
    view.on_event(MessageUpdate(
        message=msg,
        assistantMessageEvent=AssistantMessageEvent(type="error", error="rate limit"),
    ))
    assert view._error == "rate limit"


def test_stream_view_print_final(capsys):
    console = Console(force_terminal=False, no_color=True)
    view = StreamView(console)
    view._text_parts = ["Hello **world**"]
    view._tools["t1"] = ToolStatus(
        name="bash", args_summary="ls", status="done", duration=0.5,
    )

    view.print_final(console)
    captured = capsys.readouterr()
    assert "world" in captured.out
    assert "bash" in captured.out


def test_render_tool_running():
    view, _ = _make_view()
    ts = ToolStatus(name="read_file", args_summary="main.py")
    result = view._render_tool(ts)
    assert isinstance(result, Text)
    assert "read_file" in str(result)


def test_render_tool_done():
    view, _ = _make_view()
    ts = ToolStatus(name="bash", args_summary="ls", status="done", duration=1.2)
    result = view._render_tool(ts)
    text = str(result)
    assert "\u2713" in text
    assert "1.2s" in text


def test_render_tool_error():
    view, _ = _make_view()
    ts = ToolStatus(name="bash", args_summary="ls", status="error", is_error=True, duration=0.5)
    result = view._render_tool(ts)
    text = str(result)
    assert "\u2717" in text


def test_summarize_args_path():
    assert _summarize_args({"path": "src/main.py"}) == "src/main.py"


def test_summarize_args_command():
    assert _summarize_args({"command": "pytest tests/"}) == "pytest tests/"


def test_summarize_args_truncates():
    long = "x" * 100
    result = _summarize_args({"path": long})
    assert len(result) <= 63


def test_summarize_args_empty():
    assert _summarize_args({}) == ""


def test_summarize_args_fallback_string():
    assert _summarize_args({"count": 5, "label": "hello"}) == "hello"
