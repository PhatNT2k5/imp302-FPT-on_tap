# Lecture video builder

Renders the narrated Vietnamese lecture videos shown in "Học kiến thức".

Two script formats live side by side while chapters are being rewritten:

- **Story script** (new, chapter 5 so far): one short video per method, told as a story (see "Story template"). Output: `../media/lectures/chNN/NN-<id>.*`.
- **Chapter script** (old, other chapters): one long video per chapter. Output: `../media/lectures/chNN.*`.

The site player (`../lecture-video.js`) shows a playlist for story chapters and a single video for the rest.

## Files

| File | Role |
| --- | --- |
| `scripts/chNN.json` | Lecture script per chapter (formats below) |
| `story_gen/gen_chNN.py` | Python generators that write each story script and its story map (shared helpers in `story_kit.py`) |
| `story_maps/chNN.md` | Method map of a chapter: order, problem → old way → idea → limit → next. Reviewed before writing the script |
| `script_model.py` | Pydantic schema, beat-order rules, asset checks (slide pages, image paths, TTS-friendly narration, story length) |
| `slide_template.html` | The slide layout; KaTeX renders `$...$` math (vendored in `vendor/katex`); SVG drawing for graph / histogram / intervals |
| `slides.py` | Turns each video (`Unit`) into one frame state per narration segment and screenshots it with Edge/Chrome via Playwright |
| `build_lecture.py` | TTS (edge-tts, `vi-VN-HoaiMyNeural`) + frames + ffmpeg → `../media/lectures/…{mp4,vtt,chapters.vtt,webp}` and `../lecture-data.js` |
| `validate_scripts.py` | Validate scripts: `python -I validate_scripts.py [chapters]` (prints estimated minutes per story) |
| `check_overflow.py` | Lay out every frame and report text that does not fit its box (must be 0) |
| `preview.py` | Save PNGs of scenes to `cache/preview/`: `preview.py 5 huffman [scenes] [--all-frames]` |
| `verify_examples.py` | Recompute every number used in the worked examples |
| `cache/` | TTS audio cache keyed by text (editing one segment only re-synthesizes that segment), rendered slide pages, frames |

## Story template

Every method video tells the same story, in this order (`kicker` of each scene):

| # | Beat | Answers | Required |
| --- | --- | --- | --- |
| 1 | `Vấn đề` | What problem are we facing? Tie it to the chapter's running example | ✓ |
| 2 | `Cách cũ` | How was it done before, and where does that fall short? Picks up the previous video's `Hạn chế` | ✓ (not for the first method) |
| 3 | `Ý tưởng` | The core idea in one sentence + an everyday analogy, no formula yet | ✓ |
| 4 | `Cách làm` | Step by step on a small numeric example, the visual moves with the narration | ✓ |
| 4 | `Công thức` | After the intuition; annotate with `\underbrace{…}_{\text{meaning}}` | if the slides have one |
| 5 | `So sánh` | What it wins / trades off against the previous method (table) | ✓ |
| 6 | `Ứng dụng` | Where it is used | ✓ |
| 7 | `Hạn chế` | What is still missing → leads into the next video (show `chain`) | ✓ |
| 8 | `Bẫy thi` | 1–4 exam traps for this method | ✓ |

Beats may repeat (several `Cách làm` scenes) but never go backwards; `Cách làm` and `Công thức` may interleave.
`extra` stories (short side topics) need only `Vấn đề`, `Ý tưởng`, `Bẫy thi`. Each chapter also has an `intro` story (first kicker `Mở đầu`) and a `summary` story (a `Tổng kết` scene).

Rules:
- One **running example** for the whole chapter (`example` field), every story comes back to it.
- **Guess first:** put `"ask": true` on a point before revealing an answer; it shows a "Thử đoán trước" badge and adds a 2 s pause (`pause` overrides).
- **Faithful to the slides:** definitions, formulas and numbers follow `../references/` and `lessons.txt`; every number is checked in `verify_examples.py`. Applications outside the slides must be well-known facts.
- Spoken style: short sentences, "các bạn"; never read symbols aloud.
- Length (estimated by the validator): intro 0.5–2.5 min, method 1.5–6.5 min, extra 1–4.5 min, summary 0.6–3.5 min.

## Story script format

```jsonc
{
  "title": "Nén ảnh",
  "example": "Gửi ảnh bầu trời 512×512 qua mạng chậm",
  "stories": [
    {"id": "huffman", "title": "Mã Huffman", "kind": "method",   // intro | method | extra | summary
     "scenes": [ /* scenes as below */ ]}
  ]
}
```

## Scene format (both script types)

```jsonc
{
  "kicker": "Cách làm",                  // story beat, or Recap/Intuition/... in old chapter scripts
  "title": "Huffman bước 2",
  "slide": 24,                           // optional: page of ../references/<chapter pdf>
  "image": "media/c05-slide-24.webp",    // optional: an existing file under ../media (not with slide)
  "formula": "L = \\sum p_i l_i",        // optional KaTeX display formula
  // at most ONE visual per scene:
  "table": {"headers": ["..."], "rows": [["...", "$a_2$"]]},
  "code": {"lines": ["...", "..."]},
  "grid": [{"label": "...", "cells": [[1, 2], [3, 4]], "accent": [[0, 1]], "warn": [], "dim": []}],
  "graph": {"nodes": [{"id": "r", "label": "1", "x": 5, "y": 0, "shape": "box", "step": 5}],
            "edges": [{"a": "r", "b": "x4", "label": "0", "step": 5, "marks": [{"step": 6, "style": "accent"}]}],
            "arrows": false, "caption": "..."},           // trees, pipelines (x or y constant), scatter plots (shape "dot")
  "histogram": {"bars": [{"label": "A", "value": 40}], "lines": [{"at": 2.5, "label": "T"}],
                "bands": [{"start": 3, "end": 6, "label": "dead zone", "step": 2}]},   // positions in bar units
  "intervals": {"rows": [{"low": 0, "high": 1, "parts": [["a1", 0, 0.2], ["a2", 0.2, 1]], "pick": "a1", "step": 1}]},
  "compare": {"left": {"label": "...", "grid": {...}}, "right": {"label": "...", "image": "media/..."}, "arrow": "..."},
  "chain": {"items": ["Huffman", "Mã số học"], "current": 2},   // done ✓ before current, current highlighted
  "points": [
    {"text": "bullet shown with this segment", "say": "narration", "reveal": [1, 2], "ask": false}
  ]
}
```

- `reveal` (1-based, `0` = nothing) picks the highlighted table rows, code lines, grids, or **visual steps**. Earlier items stay visible; later ones stay hidden.
- Staged visuals (`graph`, `histogram`, `intervals`): every element has `step` (appears at that reveal, 0 = from the start) and `marks` (`{"step", "style"}` with style `accent` / `warn` / `dim` / `cut`; the latest mark reached wins). Every step must be revealed by some point. `compare`: reveal 1 shows the left panel, 2 the right.
- A visual with bullets is drawn left of the bullets; `chain` sits above the bullets; `compare` takes the full width.
- A `table` without bullets and without `reveal` must have exactly one narration segment per row.
- `code` requires `reveal` on at least one segment.
- Narration: no LaTeX, and decimals written as words ("không phẩy năm") so the TTS voice reads them correctly. The validator rejects `0.5`-style digits in `say`.

## Rebuild

```bash
python -m venv .venv
.venv/Scripts/python -m pip install edge-tts pymupdf pillow imageio-ffmpeg playwright pydantic numpy
.venv/Scripts/python -I validate_scripts.py
.venv/Scripts/python -I verify_examples.py
.venv/Scripts/python -I check_overflow.py 5
.venv/Scripts/python -I preview.py 5 huffman            # look at the visuals
.venv/Scripts/python -I build_lecture.py 5              # one chapter
.venv/Scripts/python -I build_lecture.py 5 --only=huffman,jpeg   # re-render only some stories
```

Slides are rendered with the installed Microsoft Edge (or Chrome), so no `playwright install` is needed. TTS needs internet; the Microsoft endpoint randomly drops requests, so the script retries and falls back to sentence-by-sentence synthesis. The build stops if any frame overflows. Rebuilding a chapter as stories deletes its old single video.

`app.original.js`, `index.original.html`, `style.original.css` are the site files before the video player was added.
