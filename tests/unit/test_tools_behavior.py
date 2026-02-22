from pathlib import Path

import pytest

from gen_agent.models.tools import BashInput, EditInput, FindInput, GrepInput, LsInput, ReadInput, WriteInput
from gen_agent.tools.bash import BashTool
from gen_agent.tools.edit import EditTool
from gen_agent.tools.find import FindTool
from gen_agent.tools.grep import GrepTool
from gen_agent.tools.ls import LsTool
from gen_agent.tools.path_utils import resolve_read_path
from gen_agent.tools.read import ReadTool
from gen_agent.tools.write import WriteTool


@pytest.mark.asyncio
async def test_write_and_read_tool(tmp_path: Path) -> None:
    write_tool = WriteTool(str(tmp_path))
    read_tool = ReadTool(str(tmp_path))

    await write_tool.execute(WriteInput(path="a.txt", content="hello"))
    content, _ = await read_tool.execute(ReadInput(path="a.txt"))
    assert "hello" in content[0].text


@pytest.mark.asyncio
async def test_edit_tool_unique_match(tmp_path: Path) -> None:
    file = tmp_path / "a.txt"
    file.write_text("one\ntwo\n", encoding="utf-8")
    tool = EditTool(str(tmp_path))
    content, details = await tool.execute(EditInput(path="a.txt", oldText="two", newText="three"))
    assert "Successfully replaced" in content[0].text
    assert "three" in file.read_text(encoding="utf-8")
    assert "diff" in details


@pytest.mark.asyncio
async def test_bash_tool_timeout(tmp_path: Path) -> None:
    tool = BashTool(str(tmp_path))
    with pytest.raises(TimeoutError) as exc:
        await tool.execute(BashInput(command="echo hi; sleep 2", timeout=1))
    assert "timed out" in str(exc.value)


@pytest.mark.asyncio
async def test_read_tool_image_output(tmp_path: Path) -> None:
    image = tmp_path / "x.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\n")
    tool = ReadTool(str(tmp_path))
    content, details = await tool.execute(ReadInput(path="x.png"))
    assert details is None
    assert content[0].type == "text"
    assert "image/png" in content[0].text
    assert content[1].type == "image"
    assert content[1].mime_type == "image/png"


@pytest.mark.asyncio
async def test_read_tool_image_magic_bytes_without_extension(tmp_path: Path) -> None:
    image = tmp_path / "imageblob"
    image.write_bytes(b"\x89PNG\r\n\x1a\n" + b"payload")
    tool = ReadTool(str(tmp_path))
    content, details = await tool.execute(ReadInput(path="imageblob"))
    assert details is None
    assert content[0].type == "text"
    assert "image/png" in content[0].text
    assert content[1].type == "image"
    assert content[1].mime_type == "image/png"


@pytest.mark.asyncio
async def test_edit_tool_preserves_bom_and_crlf(tmp_path: Path) -> None:
    file = tmp_path / "crlf.txt"
    file.write_text("\ufeffa\r\nb\r\n", encoding="utf-8")
    tool = EditTool(str(tmp_path))
    await tool.execute(EditInput(path="crlf.txt", oldText="a\nb\n", newText="x\ny\n"))
    raw_bytes = file.read_bytes()
    assert raw_bytes.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" in raw_bytes
    assert b"x\r\ny\r\n" in raw_bytes


def test_resolve_read_path_nfd_curly_variant(tmp_path: Path) -> None:
    target = tmp_path / "Cafe\u0301 d\u2019ecran.txt"
    target.write_text("ok", encoding="utf-8")
    resolved = resolve_read_path("Café d'ecran.txt", str(tmp_path))
    assert resolved.exists()
    assert resolved.read_text(encoding="utf-8") == "ok"
    assert "\u2019" in resolved.name


@pytest.mark.asyncio
async def test_grep_tool_with_limit_and_literal(tmp_path: Path) -> None:
    file = tmp_path / "a.txt"
    file.write_text("alpha\nbeta\nalpha\n", encoding="utf-8")
    tool = GrepTool(str(tmp_path))
    content, details = await tool.execute(GrepInput(path=".", pattern="alpha", literal=True, limit=1))
    text = content[0].text
    assert "a.txt:1: alpha" in text
    assert "limit reached" in text
    assert isinstance(details, dict)
    assert details.get("matchLimitReached") == 1


@pytest.mark.asyncio
async def test_find_tool_relative_paths_and_limit(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("x", encoding="utf-8")
    (tmp_path / "src" / "b.py").write_text("x", encoding="utf-8")
    tool = FindTool(str(tmp_path))
    content, details = await tool.execute(FindInput(path="src", pattern="*.py", limit=1))
    text = content[0].text
    assert "a.py" in text or "b.py" in text
    assert "src/" not in text
    assert "limit reached" in text
    assert isinstance(details, dict)
    assert details.get("resultLimitReached") == 1


@pytest.mark.asyncio
async def test_ls_tool_directory_suffix_and_limit(tmp_path: Path) -> None:
    (tmp_path / "dir").mkdir()
    (tmp_path / "file.txt").write_text("x", encoding="utf-8")
    tool = LsTool(str(tmp_path))
    content, details = await tool.execute(LsInput(path=".", limit=1))
    text = content[0].text
    assert "entries limit reached" in text
    assert "dir/" in text or "file.txt" in text
    assert isinstance(details, dict)
    assert details.get("entryLimitReached") == 1
