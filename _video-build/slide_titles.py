"""Dump the first meaningful lines of every slide page, so lecture scenes can reference real slides."""
import io
import sys
from pathlib import Path

import pymupdf as fitz

REFS = Path(__file__).resolve().parent.parent / "references"
OUT = Path(__file__).resolve().parent / "slide_titles.txt"


def page_summary(page: fitz.Page) -> str:
    lines = [ln.strip() for ln in page.get_text().splitlines() if len(ln.strip()) > 2]
    return " | ".join(lines[:2])[:70]


def main() -> None:
    out: list[str] = []
    for pdf in sorted(REFS.glob("[0-9][0-9]-*.pdf")):
        with fitz.open(pdf) as doc:
            out.append(f"### {pdf.name} ({doc.page_count} pages)")
            out.extend(f"{i + 1}: {page_summary(p)}" for i, p in enumerate(doc))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(out))
    print(f"wrote {OUT} ({len(out)} lines)", file=sys.stderr)


if __name__ == "__main__":
    main()
