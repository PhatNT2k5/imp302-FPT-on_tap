# Lecture video builder

Renders the 12 narrated Vietnamese lecture videos shown in "Học kiến thức".

- `scripts/chNN.json` — lecture script per chapter: scenes → points (`text` = bullet on screen, `say` = narration). `slide` is a page number in `../references/`.
- `build_lecture.py` — TTS (edge-tts, voice `vi-VN-HoaiMyNeural`) + frame rendering (Pillow, PyMuPDF) + encoding (bundled ffmpeg). Writes `../media/lectures/chNN.{mp4,vtt,webp}` and `../lecture-data.js`.
- `cache/` — TTS audio cache keyed by text, so editing one point only re-synthesizes that point.

## Rebuild

```bash
python -m venv .venv
.venv/Scripts/python -m pip install edge-tts pymupdf pillow imageio-ffmpeg
.venv/Scripts/python -I build_lecture.py        # all chapters
.venv/Scripts/python -I build_lecture.py 3 5    # only chapters 3 and 5
```

Needs internet for TTS. The Microsoft TTS endpoint randomly drops requests; the script retries and falls back to sentence-by-sentence synthesis.

`app.original.js`, `index.original.html`, `style.original.css` are the site files before the video player was added.
