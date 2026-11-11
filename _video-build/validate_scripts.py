"""Validate chapter scripts: schema, reveal counts, slide pages, image paths, TTS-friendly narration.

Usage: python -I validate_scripts.py [chapters...]   (no args = every script)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # `python -I` leaves the script folder off sys.path

from pydantic import ValidationError

from script_model import SCRIPTS, check_assets, load_script


def validate(chapter: int) -> list[str]:
    try:
        script = load_script(chapter)
    except ValidationError as exc:
        return [f"ch{chapter:02d}: {err['msg']} at {'.'.join(str(p) for p in err['loc'])}" for err in exc.errors()]
    except (OSError, ValueError) as exc:
        return [f"ch{chapter:02d}: {exc}"]
    return check_assets(chapter, script)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    chapters = [int(a) for a in sys.argv[1:]] or sorted(int(p.stem[2:]) for p in SCRIPTS.glob("ch*.json"))
    failed = 0
    for chapter in chapters:
        problems = validate(chapter)
        failed += bool(problems)
        if problems:
            print("\n".join(problems))
        else:
            script = load_script(chapter)
            points = sum(len(s.points) for s in script.scenes)
            print(f"ch{chapter:02d}: ok ({len(script.scenes)} scenes, {points} narration segments)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
