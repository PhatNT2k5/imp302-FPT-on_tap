"""Save PNG previews of chosen slides so they can be checked by eye.

Usage: python -I preview.py CHAPTER [scene numbers...]
Without scene numbers, previews every scene that has a formula, table, code or grid.
Each preview shows the last frame of the scene (everything revealed). Output: cache/preview/.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # `python -I` leaves the script folder off sys.path

from script_model import ROOT, load_script
from slides import Frame, draw, frame_state, slide_page

OUT = ROOT / "cache" / "preview"


async def main(chapter: int, wanted: list[int]) -> None:
    script = load_script(chapter)
    scenes = wanted or [n for n, s in enumerate(script.scenes, start=1) if s.formula or s.table or s.code or s.grid]
    OUT.mkdir(parents=True, exist_ok=True)
    async with slide_page() as page:
        for n in scenes:
            last = len(script.scenes[n - 1].points) - 1
            png = OUT / f"ch{chapter:02d}-s{n:02d}.png"
            problems = await draw(page, Frame(n - 1, last, frame_state(chapter, script, n - 1, last)), png)
            print(png, "| overflow:" if problems else "", "; ".join(problems))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main(int(sys.argv[1]), [int(a) for a in sys.argv[2:]]))
