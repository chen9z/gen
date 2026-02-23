from __future__ import annotations

import asyncio
import signal

import pytest

from gen_agent.extensions import CustomEditorComponent
from gen_agent.interactive.ptk_app import GenInteractiveApp, PtkExtensionUIContext, run_interactive_mode


class _DummyRunner:
    def get_commands(self):
        return {}


class _DummySession:
    def __init__(self) -> None:
        self.cwd = "/tmp"
        self.extension_runner = _DummyRunner()
        self.ui_extensions_enabled = False

    def bind_ui_context(self, _context) -> None:
        return

    def subscribe(self, _listener):
        return lambda: None

    def get_state(self):
        return {
            "provider": "openai",
            "modelId": "gpt-4o-mini",
            "thinkingLevel": "off",
            "sessionName": "demo",
            "pendingMessageCount": 0,
        }

    async def prompt(self, _payload: str):
        return []


class _DummyApp:
    def __init__(self) -> None:
        self.notifies: list[tuple[str, str]] = []
        self.status: dict[str, str | None] = {}
        self.widgets: dict[str, tuple[list[str] | None, str]] = {}
        self.header: list[str] | None = None
        self.footer: list[str] | None = None
        self.title: str | None = None
        self.editor_text = ""
        self.editor_component = None

    def notify(self, message: str, level: str = "info") -> None:
        self.notifies.append((message, level))

    def set_status(self, key: str, text: str | None) -> None:
        self.status[key] = text

    def set_widget(self, key: str, lines: list[str] | None, placement: str = "above_editor") -> None:
        self.widgets[key] = (lines, placement)

    def set_header(self, lines: list[str] | None) -> None:
        self.header = lines

    def set_footer(self, lines: list[str] | None) -> None:
        self.footer = lines

    def set_title(self, title: str) -> None:
        self.title = title

    def get_editor_text(self) -> str:
        return self.editor_text

    def set_editor_text(self, text: str) -> None:
        self.editor_text = text

    def set_editor_component(self, component: CustomEditorComponent | None) -> None:
        self.editor_component = component



def test_ptk_extension_context_accepts_text_api() -> None:
    app = _DummyApp()
    ctx = PtkExtensionUIContext(app)

    ctx.notify("hello", level="warning")
    ctx.set_status("sync", "ok")
    ctx.set_widget("w-top", ["A", "B"], placement="above_editor")
    ctx.setWidget("w-bottom", "C", {"placement": "belowEditor"})
    ctx.set_header("H")
    ctx.set_footer(["F1", "F2"])
    ctx.set_title("My title")
    ctx.set_editor_text("seed")
    ctx.set_editor_component(CustomEditorComponent(placeholder="p", title="t", status_hint="h"))

    assert app.notifies[-1] == ("hello", "warning")
    assert app.status["sync"] == "ok"
    assert app.widgets["w-top"] == (["A", "B"], "above_editor")
    assert app.widgets["w-bottom"] == (["C"], "below_editor")
    assert app.header == ["H"]
    assert app.footer == ["F1", "F2"]
    assert app.title == "My title"
    assert ctx.get_editor_text() == "seed"
    assert isinstance(app.editor_component, CustomEditorComponent)



def test_ptk_extension_context_rejects_non_text_content() -> None:
    app = _DummyApp()
    ctx = PtkExtensionUIContext(app)

    with pytest.raises(TypeError):
        ctx.set_widget("w", object())
    with pytest.raises(TypeError):
        ctx.set_header({"x": 1})
    with pytest.raises(TypeError):
        ctx.set_footer(["ok", 1])
    with pytest.raises(TypeError):
        ctx.set_editor_component("invalid")


@pytest.mark.asyncio
async def test_run_interactive_mode_instantiates_ptk_app(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {"value": False}

    async def _fake_run(self):
        called["value"] = True
        return 0

    monkeypatch.setattr("gen_agent.interactive.ptk_app.sys.stdin.isatty", lambda: True)
    monkeypatch.setattr("gen_agent.interactive.ptk_app.sys.stdout.isatty", lambda: True)
    monkeypatch.setattr("gen_agent.interactive.ptk_app.GenInteractiveApp.run_async", _fake_run)

    code = await run_interactive_mode(_DummySession(), initial_message="hello")
    assert code == 0
    assert called["value"] is True


@pytest.mark.asyncio
async def test_run_interactive_mode_falls_back_to_print_when_not_tty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("gen_agent.interactive.ptk_app.sys.stdin.isatty", lambda: False)
    monkeypatch.setattr("gen_agent.interactive.ptk_app.sys.stdout.isatty", lambda: False)

    async def _fake_print(session, message=None):
        _ = session
        assert message == "hello"
        return 0

    monkeypatch.setattr("gen_agent.modes.print_mode.run_print_mode", _fake_print)
    code = await run_interactive_mode(_DummySession(), initial_message="hello")
    assert code == 0


def test_interactive_prompt_prefix_uses_single_style() -> None:
    app = GenInteractiveApp(_DummySession())
    assert app._editor_prompt_prefix() == "› "
    assert "Ctrl+C interrupt" in app._prompt_status()

    app.set_editor_component(CustomEditorComponent(placeholder="input"))
    assert app._editor_prompt_prefix() == "› input: "


class _InterruptibleSession(_DummySession):
    def __init__(self) -> None:
        super().__init__()
        self.started = asyncio.Event()
        self.cancelled = False

    async def prompt(self, _payload: str):
        self.started.set()
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            self.cancelled = True
            return []
        return []


@pytest.mark.asyncio
async def test_submit_ctrl_c_cancels_active_run_and_restores_signal(monkeypatch: pytest.MonkeyPatch) -> None:
    session = _InterruptibleSession()
    app = GenInteractiveApp(session)

    current_handler = object()
    installed: list[object] = []
    signal_handler: dict[str, object] = {}

    def _fake_getsignal(_sig: signal.Signals):
        return current_handler

    def _fake_signal(_sig: signal.Signals, handler):
        installed.append(handler)
        signal_handler["value"] = handler
        return current_handler

    monkeypatch.setattr("gen_agent.interactive.ptk_app.signal.getsignal", _fake_getsignal)
    monkeypatch.setattr("gen_agent.interactive.ptk_app.signal.signal", _fake_signal)

    submit_task = asyncio.create_task(app._submit("hello"))
    await session.started.wait()
    assert "value" in signal_handler

    handler = signal_handler["value"]
    assert callable(handler)
    handler(signal.SIGINT, None)

    assert await submit_task is True
    assert session.cancelled is True
    assert current_handler in installed
