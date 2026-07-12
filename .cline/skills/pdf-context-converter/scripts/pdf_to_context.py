#!/usr/bin/env python3
"""Convert a PDF into indexed, page-addressable Markdown and optional HTML."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

from pypdf import PdfReader

GENERATOR_ID = "pdf-context-converter"


def slug(value: str) -> str:
    result = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-.")
    return result or "document"


def status_for(text: str, error: str | None) -> str:
    if error:
        return "EXTRACTION_ERROR"
    length = len(text.strip())
    if length == 0:
        return "OCR_REQUIRED"
    if length < 100:
        return "LOW_TEXT"
    return "OK"


def page_markdown(source: str, page_number: int, text: str, status: str) -> str:
    body = text.strip() or "_抽出テキストなし。原本ページの確認またはOCRが必要です。_"
    return f"## Page {page_number}\n\n- Source: `{source}`\n- Status: `{status}`\n\n{body}\n"


def remove_previous_output(input_path: Path, output_dir: Path) -> None:
    resolved_input = input_path.resolve()
    resolved_output = output_dir.resolve()
    protected = {Path.cwd().resolve(), Path.home().resolve(), resolved_input.parent}
    if resolved_output in protected or resolved_output == Path(resolved_output.anchor):
        raise ValueError(f"危険な出力先は上書きできません: {output_dir}")
    if resolved_output in resolved_input.parents:
        raise ValueError(f"入力PDFを含む出力先は上書きできません: {output_dir}")

    marker = output_dir / "metadata.json"
    if not marker.is_file():
        raise ValueError(f"このツールの生成物と確認できないため上書きできません: {output_dir}")
    try:
        metadata = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"生成物メタデータを検証できません: {marker}") from exc
    if metadata.get("generated_by") != GENERATOR_ID:
        raise ValueError(f"このツールの生成物と確認できないため上書きできません: {output_dir}")
    shutil.rmtree(output_dir)


def convert(input_path: Path, output_dir: Path, output_format: str, pages_per_chunk: int, overwrite: bool) -> dict:
    if not input_path.is_file():
        raise FileNotFoundError(f"入力PDFがありません: {input_path}")
    if input_path.suffix.lower() != ".pdf":
        raise ValueError("入力ファイルは.pdfである必要があります")
    if pages_per_chunk < 1:
        raise ValueError("pages-per-chunkは1以上である必要があります")
    if output_dir.exists():
        if not overwrite:
            raise FileExistsError(f"出力先が存在します。置換する場合は--overwriteを指定してください: {output_dir}")
        remove_previous_output(input_path, output_dir)

    sections = output_dir / "sections"
    sections.mkdir(parents=True)
    reader = PdfReader(str(input_path))
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        error = None
        try:
            text = page.extract_text() or ""
        except Exception as exc:  # Preserve the page in the manifest even when extraction fails.
            text = ""
            error = f"{type(exc).__name__}: {exc}"
        pages.append({"page": number, "text": text, "chars": len(text.strip()), "status": status_for(text, error), "error": error})

    chunks = []
    for offset in range(0, len(pages), pages_per_chunk):
        group = pages[offset : offset + pages_per_chunk]
        start, end = group[0]["page"], group[-1]["page"]
        filename = f"pages-{start:04d}-{end:04d}.md"
        header = f"# {input_path.name}: pages {start}-{end}\n\nSource: `{input_path.name}`, pages {start}-{end}\n\n"
        content = header + "\n".join(page_markdown(input_path.name, p["page"], p["text"], p["status"]) for p in group)
        (sections / filename).write_text(content, encoding="utf-8")
        chunks.append({"file": f"sections/{filename}", "start_page": start, "end_page": end, "chars": sum(p["chars"] for p in group)})

    counts = {key: sum(p["status"] == key for p in pages) for key in ("OK", "LOW_TEXT", "OCR_REQUIRED", "EXTRACTION_ERROR")}
    digest = hashlib.sha256(input_path.read_bytes()).hexdigest()
    metadata = {
        "generated_by": GENERATOR_ID,
        "source": str(input_path), "source_sha256": digest, "pages": len(pages),
        "chunks": chunks, "status_counts": counts,
        "page_status": [{k: p[k] for k in ("page", "chars", "status", "error")} for p in pages],
        "format": output_format,
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rows = "\n".join(f"| [{c['file']}]({c['file']}) | {c['start_page']}-{c['end_page']} | {c['chars']} |" for c in chunks)
    index = f"""# {input_path.name} Context Index

- Source: `{input_path}`
- SHA-256: `{digest}`
- Pages: {len(pages)}
- Status: {', '.join(f'{k}={v}' for k, v in counts.items())}

## Retrieval

この索引を先に読み、検索後に必要なチャンクだけを開く。原本PDFが正本であり、表・図・数式・配置は原本と照合する。

| Chunk | Pages | Characters |
|---|---:|---:|
{rows}
"""
    (output_dir / "index.md").write_text(index, encoding="utf-8")

    if output_format in {"html", "both"}:
        sections_html = []
        for p in pages:
            escaped = html.escape(p["text"].strip()).replace("\n", "<br>\n") or "<em>抽出テキストなし。原本確認またはOCRが必要です。</em>"
            sections_html.append(f'<section id="page-{p["page"]}" data-status="{p["status"]}"><h2>Page {p["page"]}</h2><p><strong>Status:</strong> {p["status"]}</p><div>{escaped}</div></section>')
        document = "<!doctype html>\n<html lang=\"ja\"><meta charset=\"utf-8\"><title>" + html.escape(input_path.name) + "</title><body><main>" + "\n".join(sections_html) + "</main></body></html>\n"
        (output_dir / "document.html").write_text(document, encoding="utf-8")
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--format", choices=("markdown", "html", "both"), default="markdown")
    parser.add_argument("--pages-per-chunk", type=int, default=5)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    metadata = convert(args.input, args.output_dir, args.format, args.pages_per_chunk, args.overwrite)
    print(json.dumps({"output": str(args.output_dir), "pages": metadata["pages"], "status_counts": metadata["status_counts"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
