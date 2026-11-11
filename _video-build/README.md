# Lecture video builder

Renders the 12 narrated Vietnamese lecture videos shown in "Học kiến thức".

## Files

| File | Role |
| --- | --- |
| `scripts/chNN.json` | Lecture script per chapter (format below) |
| `script_model.py` | Pydantic schema + asset checks (slide pages, image paths, TTS-friendly narration) |
| `slide_template.html` | The slide layout; KaTeX renders `$...$` math (vendored in `vendor/katex`, no network needed) |
| `slides.py` | Turns a script into one frame state per narration segment and screenshots it with Edge/Chrome via Playwright; also LaTeX → Unicode for outline titles |
| `build_lecture.py` | TTS (edge-tts, `vi-VN-HoaiMyNeural`) + frames + ffmpeg → `../media/lectures/chNN.{mp4,vtt,chapters.vtt,webp}` and `../lecture-data.js` |
| `validate_scripts.py` | Validate scripts: `python -I validate_scripts.py [chapters]` |
| `check_overflow.py` | Lay out every frame and report text that does not fit its box (must be 0) |
| `preview.py` | Save PNGs of chosen scenes to `cache/preview/` for a visual check |
| `verify_examples.py` | Recompute every number used in the worked examples of chapters 5–12 |
| `cache/` | TTS audio cache keyed by text (editing one segment only re-synthesizes that segment), rendered slide pages, frames |

## Script format

```jsonc
{
  "title": "Nén ảnh",
  "scenes": [
    {
      "kicker": "Worked example",        // optional label above the title
      "title": "Huffman bước 2",
      "slide": 24,                       // optional: page of ../references/<chapter pdf>
      "image": "media/c05-slide-24.webp",// optional: an existing file under ../media (not with slide)
      "formula": "L = \\sum p_i l_i",    // optional KaTeX display formula
      "table": {"headers": ["..."], "rows": [["...", "$a_2$"]]},  // cells may contain $LaTeX$
      "code": {"lines": ["...", "..."]}, // pseudocode with line numbers
      "grid": [{"label": "...", "cells": [[1, 2], [3, 4]], "accent": [[0, 1]], "warn": [], "dim": []}],
      "points": [
        {"text": "bullet shown with this segment", "say": "narration", "reveal": [1, 2]}
      ]
    }
  ]
}
```

- Every field except `title`, `points` and `say` is optional; old scripts (bullets + `slide`) still work.
- `kicker`: `Recap`, `Intuition`, `Formula`, `Worked example`, `Algorithm`, `Compare`, `Exam traps`, `Summary`.
- One scene uses at most one of `table` / `code` / `grid`.
- `reveal` (1-based, `0` = nothing) picks the highlighted table rows, code lines or grids for that segment. Earlier rows stay visible; later ones stay hidden.
- A `table` without bullets and without `reveal` must have exactly one narration segment per row; each segment shows one more row and highlights it.
- `code` requires `reveal` on at least one segment.
- Narration: no LaTeX, and decimals written as words ("không phẩy năm") so the TTS voice reads them correctly. The validator rejects `0.5`-style digits in `say`.

## Teaching template for hard chapters (5–12)

1. **Recap** – what earlier chapters gave us and what this chapter reuses.
2. **Intuition** – an everyday example before any formula.
3. **Formula** – annotate parts with `\underbrace{...}_{\text{meaning}}`; narration explains meaning, never reads symbols.
4. **Worked example** – concrete numbers, one row/slide per step, no skipped steps; numbers checked in `verify_examples.py`.
5. **Algorithm** – pseudocode, narration walks through the key lines.
6. **Compare** – table against easily confused methods.
7. **Exam traps** – 4–5 question/answer rows.
8. **Summary** – recap plus a lead-in to the next chapter.

Content must follow the original slides in `../references/` and the summary in `lessons.txt`.

## Rebuild

```bash
python -m venv .venv
.venv/Scripts/python -m pip install edge-tts pymupdf pillow imageio-ffmpeg playwright pydantic numpy
.venv/Scripts/python -I validate_scripts.py
.venv/Scripts/python -I check_overflow.py 5 6
.venv/Scripts/python -I build_lecture.py        # all chapters
.venv/Scripts/python -I build_lecture.py 3 5    # only chapters 3 and 5
```

Slides are rendered with the installed Microsoft Edge (or Chrome), so no `playwright install` is needed. TTS needs internet; the Microsoft endpoint randomly drops requests, so the script retries and falls back to sentence-by-sentence synthesis. The build stops if any frame overflows.

`app.original.js`, `index.original.html`, `style.original.css` are the site files before the video player was added.
