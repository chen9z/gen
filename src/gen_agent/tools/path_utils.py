from __future__ import annotations

from pathlib import Path

UNICODE_SPACES = [
    "\u00A0",
    "\u2000",
    "\u2001",
    "\u2002",
    "\u2003",
    "\u2004",
    "\u2005",
    "\u2006",
    "\u2007",
    "\u2008",
    "\u2009",
    "\u200A",
    "\u202F",
    "\u205F",
    "\u3000",
]


def normalize_spaces(value: str) -> str:
    out = value
    for ch in UNICODE_SPACES:
        out = out.replace(ch, " ")
    return out


def expand_path(path: str) -> str:
    path = normalize_spaces(path)
    if path.startswith("@"):
        path = path[1:]
    if path == "~":
        return str(Path.home())
    if path.startswith("~/"):
        return str(Path.home() / path[2:])
    return path


def resolve_to_cwd(path: str, cwd: str) -> Path:
    expanded = expand_path(path)
    p = Path(expanded)
    if p.is_absolute():
        return p
    return Path(cwd).resolve() / p


def resolve_read_path(path: str, cwd: str) -> Path:
    resolved = resolve_to_cwd(path, cwd)
    if resolved.exists():
        return resolved

    candidate = Path(str(resolved).replace(" AM.", "\u202fAM.").replace(" PM.", "\u202fPM."))
    if candidate.exists():
        return candidate

    nfd = Path(str(resolved).encode("utf-8").decode("utf-8"))
    if nfd.exists():
        return nfd

    curly = Path(str(resolved).replace("'", "\u2019"))
    if curly.exists():
        return curly

    nfd_curly = Path(str(nfd).replace("'", "\u2019"))
    if nfd_curly.exists():
        return nfd_curly

    return resolved


def is_within(path: Path, base: Path) -> bool:
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
