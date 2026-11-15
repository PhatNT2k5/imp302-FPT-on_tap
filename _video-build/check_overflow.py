"""Lay out every frame of the given chapters in the browser and report text that does not fit.

Usage: python -I check_overflow.py [chapters...]   (no args = every script). Exit code 1 if anything overflows.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # `python -I` leaves the script folder off sys.path

from script_model import SCRIPTS, load_units
from slides import draw, slide_page, unit_frames


async def main(chapters: list[int]) -> int:
    total = 0
    async with slide_page() as page:
        for chapter in chapters:
            frames_seen, found = 0, {}
            for unit in load_units(chapter):
                frames = unit_frames(unit)
                frames_seen += len(frames)
                for frame in frames:
                    for problem in await draw(page, frame):
                        found[f"  {unit.stem} '{unit.scenes[frame.scene_index].title}': {problem}"] = None
            total += len(found)
            print(f"ch{chapter:02d}: {frames_seen} frames, {len(found)} overflow problems")
            if found:
                print("\n".join(found))
    return 1 if total else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    requested = [int(a) for a in sys.argv[1:]] or sorted(int(p.stem[2:]) for p in SCRIPTS.glob("ch*.json"))
    raise SystemExit(asyncio.run(main(requested)))
