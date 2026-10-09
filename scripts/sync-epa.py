#!/usr/bin/env python3
"""Prepare a reviewable EPA snapshot for EPA-page; does not publish or push."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = (
    ("research/README.md", "Pipeline de pesquisa", "pipeline"),
    ("research/reports/initial_pipeline_summary.md", "Relatório técnico inicial", "relatorio-inicial"),
)


def inline(text: str) -> str:
    value = html.escape(text, quote=False)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    return value


def render_markdown(source: str) -> str:
    output: list[str] = []
    paragraph: list[str] = []
    list_type = ""
    code: list[str] | None = None

    def flush_paragraph() -> None:
        if paragraph:
            output.append("<p>" + inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = ""

    for raw in source.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            flush_paragraph()
            close_list()
            if code is None:
                code = []
            else:
                output.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
                code = None
            continue
        if code is not None:
            code.append(raw)
            continue
        if not line:
            flush_paragraph()
            close_list()
            continue
        match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if match:
            flush_paragraph()
            close_list()
            level = min(len(match.group(1)) + 1, 4)
            output.append(f"<h{level}>{inline(match.group(2))}</h{level}>")
            continue
        if line.startswith("> "):
            flush_paragraph()
            close_list()
            output.append("<blockquote>" + inline(line[2:]) + "</blockquote>")
            continue
        item = re.match(r"^([-*]|\d+\.)\s+(.+)$", line)
        if item:
            flush_paragraph()
            kind = "ol" if item.group(1).endswith(".") else "ul"
            if list_type != kind:
                close_list()
                output.append(f"<{kind}>")
                list_type = kind
            output.append("<li>" + inline(item.group(2)) + "</li>")
            continue
        paragraph.append(line)

    flush_paragraph()
    close_list()
    if code is not None:
        output.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
    return "\n".join(output)


def git_value(source: Path, fmt: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(source), "log", "-1", f"--format={fmt}"],
        text=True,
        encoding="utf-8",
    ).strip()


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/sync-epa.py <EPA-checkout>", file=sys.stderr)
        return 2
    source = Path(sys.argv[1]).resolve()
    if not source.is_dir():
        print(f"EPA checkout not found: {source}", file=sys.stderr)
        return 2

    template = (ROOT / "templates/document.html").read_text(encoding="utf-8")
    for relative, title, slug in DOCS:
        path = source / relative
        if not path.is_file():
            print(f"Missing source document: {path}", file=sys.stderr)
            return 1
        rendered = template.replace("{{TITLE}}", html.escape(title)).replace(
            "{{SOURCE}}", html.escape(relative)
        ).replace("{{BODY}}", render_markdown(path.read_text(encoding="utf-8")))
        target = ROOT / "site/documentos" / slug / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")

    commit = git_value(source, "%H")
    status = {
        "commit": commit,
        "subject": git_value(source, "%s"),
        "committed_at": git_value(source, "%cI"),
        "url": f"https://github.com/Carlosfrancog/Analise-Preditiva-de-Dados-Educacionais/commit/{commit}",
    }
    (ROOT / "site/assets/project-status.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Prepared {len(DOCS)} documents and status for EPA commit {commit[:7]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
