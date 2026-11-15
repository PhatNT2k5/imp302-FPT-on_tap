"""Save PNG previews of chosen slides so they can be checked by eye.

Usage: python -I preview.py CHAPTER [story-id] [scene numbers...] [--all-frames]
  - old chapter script: scene numbers count over the whole chapter.
  - story script: give a story id; without one, every story is previewed.
Without scene numbers, previews every scene that has a formula or a visual (table, code, grid, graph, ...).
Each preview shows the last frame of the scene; --all-frames saves every frame instead. Output: cache/preview/.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # `python -I` leaves the script folder off sys.path

from script_model import ROOT, load_units
from slides import Frame, draw, frame_state, slide_page

OUT = ROOT / "cache" / "preview"


async def main(chapter: int, story: str | None, wanted: list[int], every_frame: bool) -> None:
    units = [u for u in load_units(chapter) if story is None or u.stem.endswith(f"-{story}")]
    if not units:
        raise SystemExit(f"no story '{story}' in chapter {chapter}")
    OUT.mkdir(parents=True, exist_ok=True)
    async with slide_page() as page:
        for unit in units:
            scenes = wanted or [n for n, s in enumerate(unit.scenes, start=1) if s.formula or s.visual()]
            for n in scenes:
                points = range(len(unit.scenes[n - 1].points)) if every_frame else [len(unit.scenes[n - 1].points) - 1]
                for p in points:
                    suffix = f"-p{p + 1:02d}" if every_frame else ""
                    png = OUT / f"{unit.stem.replace('/', '_')}-s{n:02d}{suffix}.png"
                    problems = await draw(page, Frame(n - 1, p, frame_state(unit, n - 1, p)), png)
                    print(png, "| overflow:" if problems else "", "; ".join(problems))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if a != "--all-frames"]
    story = args[1] if len(args) > 1 and not args[1].isdigit() else None
    numbers = [int(a) for a in args[1:] if a.isdigit()]
    asyncio.run(main(int(args[0]), story, numbers, "--all-frames" in sys.argv))
