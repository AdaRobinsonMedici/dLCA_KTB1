#!/usr/bin/env python3
"""Offline repository hygiene checks; this does not validate scientific results.

Uses only the Python standard library. No notebook cells, MATLAB models, network
requests, or scientific programs are executed. Git, when available, is used only
to list tracked and non-ignored files. Markdown support is intentionally
limited to ordinary inline links and reference definitions, not a full renderer.
The credential check is a conservative heuristic, not a security audit.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote
import xml.etree.ElementTree as ET


SKIP_DIRECTORIES = {".git", ".venv", "venv", "node_modules", "__pycache__", ".ipynb_checkpoints"}
LOCAL_DIRECTORIES = {"data/local", "model/local", "results"}
TEXT_SUFFIXES = {".py", ".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".ini", ".cfg", ".m", ".sh", ".cff", ".example"}
LINK = re.compile(
    r'\]\(\s*(?P<target><[^>\n]+>|(?:\\.|[^\s()])+(?:\([^()\n]*\)[^\s()]*)*)'
    r'(?:\s+(?:"[^"\n]*"|\x27[^\x27\n]*\x27))?\s*\)'
)
REFERENCE = re.compile(r'^\s{0,3}\[[^\]\n]+\]:\s*(?P<target><[^>\n]+>|\S+)', re.MULTILINE)
LITERAL_CREDENTIAL = re.compile(
    r'''(?i)^[ \t]*(?:export[ \t]+)?["']?'''
    r'''(?P<name>(?:[a-z0-9]+[_-])*(?:api[_-]?key|token|password|passwd|client[_-]?secret|secret[_-]?key|secret))'''
    r'''["']?[ \t]*(?:=|:)[ \t]*(?:[ru])?(?P<quote>["'])(?P<value>[^\r\n]*?)(?P=quote)'''
)
ENV_CREDENTIAL = re.compile(
    r"(?i)^[ \t]*(?:export[ \t]+)?(?P<name>(?:[a-z0-9]+[_-])*(?:api[_-]?key|token|password|passwd|client[_-]?secret|secret[_-]?key|secret))[ \t]*=[ \t]*(?P<value>[^#\r\n]*)"
)


def issue(path: Path, root: Path, message: str) -> str:
    """Report location and problem only; never include source snippets or secrets."""
    return f"{path.relative_to(root).as_posix()}: {message}"


def is_placeholder(value: str) -> bool:
    value = value.strip()
    if not value:
        return True
    return bool(
        re.fullmatch(r"<[^<>]+>|\$\{[^}]+\}|\$[A-Z_][A-Z0-9_]*", value)
        or re.fullmatch(r"(?i)(?:your[_ -].*|replace[_ -].*|change[_ -]?me|placeholder|redacted|example|xxx+)", value)
    )


def credential_issues(text: str, location: str, env_file: bool = False) -> list[str]:
    lines = set()
    for line_number, line in enumerate(text.splitlines(), 1):
        matches = list(LITERAL_CREDENTIAL.finditer(line))
        if env_file:
            matches.extend(ENV_CREDENTIAL.finditer(line))
        for match in matches:
            value = match.group("value").strip().strip("\"'")
            if not is_placeholder(value):
                lines.add(line_number)
    return [f"{location}: possible literal credential at line {line}; use an environment variable" for line in sorted(lines)]


def without_markdown_code(text: str) -> str:
    """Preserve line numbers while omitting code fences, inline code and comments."""
    text = re.sub(r"<!--[\s\S]*?-->", lambda m: "\n" * m.group().count("\n"), text)
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence is None and match:
            fence = match.group(1)
            lines.append("\n" if line.endswith("\n") else "")
        elif fence is not None:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
            lines.append("\n" if line.endswith("\n") else "")
        else:
            lines.append(re.sub(r"(`+).*?\1", "", line))
    return "".join(lines)


def markdown_issues(path: Path, text: str, root: Path) -> list[str]:
    clean = without_markdown_code(text)
    errors = []
    seen = set()
    for match in list(LINK.finditer(clean)) + list(REFERENCE.finditer(clean)):
        target = match.group("target").strip("<>")
        if target.startswith(("#", "//")) or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        target = unquote(re.split(r"[?#]", target, maxsplit=1)[0])
        target = re.sub(r"\\([()\[\] ])", r"\1", target)
        if not target:
            continue
        line = clean.count("\n", 0, match.start()) + 1
        if (line, target) in seen:
            continue
        seen.add((line, target))
        try:
            destination = (path.parent / target).resolve()
            relative = destination.relative_to(root)
        except (ValueError, OSError, RuntimeError):
            errors.append(issue(path, root, f"local link at line {line} escapes the repository or is invalid"))
            continue
        if ".git" in relative.parts:
            errors.append(issue(path, root, f"local link at line {line} targets Git internals"))
        elif not destination.exists():
            errors.append(issue(path, root, f"missing local link target at line {line}: {target}"))
    return errors


def notebook_issues(path: Path, text: str, root: Path) -> list[str]:
    try:
        notebook = json.loads(text)
    except (ValueError, RecursionError):
        return [issue(path, root, "invalid notebook JSON")]
    if not isinstance(notebook, dict) or notebook.get("nbformat") != 4:
        return [issue(path, root, "expected a Jupyter nbformat 4 object")]
    cells = notebook.get("cells")
    if not isinstance(cells, list) or not isinstance(notebook.get("metadata"), dict):
        return [issue(path, root, "notebook must have cells and metadata")]
    errors = []
    for index, cell in enumerate(cells, 1):
        location = f"{path.relative_to(root).as_posix()}: cell {index}"
        if not isinstance(cell, dict) or cell.get("cell_type") not in {"code", "markdown", "raw"}:
            errors.append(f"{location}: invalid cell structure")
            continue
        source = cell.get("source")
        if isinstance(source, list) and all(isinstance(part, str) for part in source):
            source = "".join(source)
        if not isinstance(source, str) or not isinstance(cell.get("metadata"), dict):
            errors.append(f"{location}: invalid source or metadata")
            continue
        if cell["cell_type"] == "code":
            if cell.get("outputs") != []:
                errors.append(f"{location}: committed code outputs must be empty")
            if "execution_count" not in cell or cell["execution_count"] is not None:
                errors.append(f"{location}: execution_count must be null")
        errors.extend(credential_issues(source, location))
    return errors


def repository_files(root: Path) -> list[Path]:
    """Include tracked files even if ignored; never inspect local ignored inputs.

    Source archives without Git use a conservative fallback excluding known
    local-data/cache directories. Git's own metadata is always excluded.
    """
    try:
        top = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            check=False, capture_output=True, timeout=10,
        )
        if top.returncode == 0 and Path(os.fsdecode(top.stdout).strip()).resolve() == root:
            listing = subprocess.run(
                ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                check=False, capture_output=True, timeout=10,
            )
            if listing.returncode == 0:
                names = {os.fsdecode(name) for name in listing.stdout.split(b"\0") if name}
                return [root / name for name in sorted(names) if ".git" not in Path(name).parts]
    except (OSError, subprocess.TimeoutExpired):
        pass
    paths = []
    for directory, directories, files in os.walk(root, followlinks=False):
        directories[:] = sorted(
            name for name in directories
            if name not in SKIP_DIRECTORIES
            and (Path(directory) / name).relative_to(root).as_posix() not in LOCAL_DIRECTORIES
        )
        for name in directories[:] + sorted(files):
            path = Path(directory) / name
            if path.is_symlink() or not path.is_dir():
                paths.append(path)
            if path.is_symlink():
                if name in directories:
                    directories.remove(name)
    return paths


def check_repository(root: Path) -> list[str]:
    root = root.resolve()
    if not root.is_dir():
        return ["Repository root is not a directory"]
    errors = []
    for path in repository_files(root):
        if path.is_symlink():
            try:
                path.resolve().relative_to(root)
            except (ValueError, OSError, RuntimeError):
                errors.append(issue(path, root, "symlink escapes the repository or is invalid"))
            continue
        if path.is_dir() or not path.exists():
            # Locally deleted tracked files are not publication content.
            continue
        extension = path.suffix.lower()
        is_env = path.name == ".env" or path.name.startswith(".env.")
        if extension not in TEXT_SUFFIXES | {".ipynb", ".svg"} and not is_env:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            errors.append(issue(path, root, "cannot read as UTF-8 text"))
            continue
        if extension == ".ipynb":
            errors.extend(notebook_issues(path, text, root))
        else:
            errors.extend(credential_issues(text, path.relative_to(root).as_posix(), env_file=is_env))
        if extension == ".md":
            errors.extend(markdown_issues(path, text, root))
        elif extension == ".svg":
            if re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", text, re.IGNORECASE):
                errors.append(issue(path, root, "SVG document types and entities are not permitted"))
                continue
            try:
                element = ET.fromstring(text)
                if element.tag not in {"svg", "{http://www.w3.org/2000/svg}svg"}:
                    errors.append(issue(path, root, "XML root is not SVG"))
            except (ET.ParseError, ValueError):
                errors.append(issue(path, root, "invalid SVG XML"))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check_repository(args.root)
    if errors:
        print("Repository hygiene checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository hygiene checks passed (not scientific or runtime validation).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
