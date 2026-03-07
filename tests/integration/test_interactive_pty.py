from __future__ import annotations

import os
import pty
import re
import select
import signal
import subprocess
import time
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[2]
_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


def _read_available(master_fd: int) -> bytes:
    chunks = bytearray()
    while True:
        ready, _, _ = select.select([master_fd], [], [], 0.05)
        if not ready:
            break
        try:
            chunk = os.read(master_fd, 65536)
        except BlockingIOError:
            break
        if not chunk:
            break
        chunks.extend(chunk)
    return bytes(chunks)


def _terminate_process(proc: subprocess.Popen[bytes]) -> None:
    if proc.poll() is not None:
        return
    os.killpg(proc.pid, signal.SIGTERM)
    try:
        proc.wait(timeout=1)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait(timeout=1)


def test_interactive_pty_start_and_quit() -> None:
    master_fd, slave_fd = pty.openpty()
    os.set_blocking(master_fd, False)
    env = os.environ.copy()
    env.setdefault("TERM", "xterm-256color")
    proc = subprocess.Popen(
        ["uv", "run", "gen"],
        cwd=_REPO_ROOT,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True,
        start_new_session=True,
        env=env,
    )
    os.close(slave_fd)

    try:
        output = bytearray()
        deadline = time.time() + 8
        prompt_seen = False
        while time.time() < deadline:
            output.extend(_read_available(master_fd))
            text = _strip_ansi(output.decode("utf-8", errors="ignore"))
            if "› " in text:
                prompt_seen = True
                break
            if proc.poll() is not None:
                break

        assert prompt_seen, _strip_ansi(output.decode("utf-8", errors="ignore"))
        os.write(master_fd, b"/quit\r")

        exit_deadline = time.time() + 8
        while time.time() < exit_deadline and proc.poll() is None:
            output.extend(_read_available(master_fd))
            time.sleep(0.1)

        text = _strip_ansi(output.decode("utf-8", errors="ignore"))
        assert text.count("gen-agent") == 1, text
        assert "/quit" in text, text
        assert proc.poll() is not None, text
        assert proc.returncode == 0, text
    finally:
        _terminate_process(proc)
        os.close(master_fd)
