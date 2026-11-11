"""Pydantic models and validation for chapter lecture scripts (scripts/chNN.json).

A script is a list of scenes. Each scene has points; each point is one narration
segment (`say`) plus what changes on screen while it is spoken:
  - `text`   : a bullet that appears with this point (optional)
  - `reveal` : which table rows / code lines / grids are highlighted (optional)

Every field beyond `title`, `points`, `text`, `say`, `slide`, `kind`, `agenda` is
optional, so scripts written for the old Pillow renderer remain valid.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Literal

import pymupdf
from pydantic import BaseModel, ConfigDict, Field, model_validator

ROOT = Path(__file__).resolve().parent
SITE = ROOT.parent
SCRIPTS = ROOT / "scripts"

SLIDE_FILES = {
    1: "01-1.-Basic-Gray-Level-Image-Processing.pdf",
    2: "02-2.-Image-and-Video-Processing.pdf",
    3: "03-3.-Image-Degradation-Restoration-and-Resconstruction.pdf",
    4: "04-4.-Image-and-Video-Analysis.pdf",
    5: "05-5.-Image-compression.pdf",
    6: "06-6.-Video-compression.pdf",
    7: "07-7.-Image-and-Video-Acquisition.pdf",
    8: "08-8.-Image-and-Video-Rendering-and-Assessment-1-.pdf",
    9: "10-9.-Image-and-Video-segmentation.pdf",
    10: "11-10.-Feature-extraction.pdf",
    11: "12-11.-Object-detection.pdf",
    12: "13-12.-Image-pattern-classification.pdf",
}

Kicker = Literal["Recap", "Intuition", "Formula", "Worked example", "Algorithm", "Compare", "Exam traps", "Summary"]
Cell = str | int | float


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Table(Strict):
    headers: list[str] = Field(min_length=1)
    rows: list[list[Cell]] = Field(min_length=1)

    @model_validator(mode="after")
    def rows_match_headers(self) -> Table:
        for i, row in enumerate(self.rows, start=1):
            if len(row) != len(self.headers):
                raise ValueError(f"table row {i} has {len(row)} cells, expected {len(self.headers)}")
        return self


class Code(Strict):
    lines: list[str] = Field(min_length=1)


class Grid(Strict):
    """A matrix drawn as square cells, e.g. a pixel block. Marks are [row, col], 0-based."""
    label: str | None = None
    cells: list[list[Cell]] = Field(min_length=1)
    accent: list[tuple[int, int]] = []
    warn: list[tuple[int, int]] = []
    dim: list[tuple[int, int]] = []

    @model_validator(mode="after")
    def marks_inside(self) -> Grid:
        width = len(self.cells[0])
        if any(len(row) != width for row in self.cells):
            raise ValueError("grid rows must all have the same length")
        for r, c in [*self.accent, *self.warn, *self.dim]:
            if not (0 <= r < len(self.cells) and 0 <= c < width):
                raise ValueError(f"grid mark [{r}, {c}] is outside the grid")
        return self


class Point(Strict):
    say: str = Field(min_length=1)
    text: str | None = None
    reveal: int | list[int] | None = None

    def revealed(self) -> list[int] | None:
        if self.reveal is None:
            return None
        return [self.reveal] if isinstance(self.reveal, int) else list(self.reveal)


class Scene(Strict):
    title: str = Field(min_length=1)
    points: list[Point] = Field(min_length=1)
    kind: Literal["intro"] | None = None
    agenda: list[str] | None = None
    kicker: Kicker | None = None
    slide: int | None = Field(default=None, ge=1)
    image: str | None = None
    formula: str | None = None
    table: Table | None = None
    code: Code | None = None
    grid: Grid | list[Grid] | None = None

    def grids(self) -> list[Grid]:
        if self.grid is None:
            return []
        return [self.grid] if isinstance(self.grid, Grid) else self.grid

    def reveal_target(self) -> tuple[str, int] | None:
        """What `reveal` indexes in this scene, and how many items it has."""
        if self.table:
            return "table row", len(self.table.rows)
        if self.code:
            return "code line", len(self.code.lines)
        if self.grid is not None:
            return "grid", len(self.grids())
        return None

    def reveal_at(self, index: int) -> list[int]:
        """Highlighted items (1-based) while point `index` is spoken."""
        explicit = self.points[index].revealed()
        if explicit is not None:
            return explicit
        target = self.reveal_target()
        has_bullets = any(p.text for p in self.points)
        has_reveals = any(p.reveal is not None for p in self.points)
        if target and target[0] == "table row" and not has_bullets and not has_reveals:
            return [min(index + 1, target[1])]  # one narration segment per row
        for earlier in range(index - 1, -1, -1):  # keep the last explicit highlight
            previous = self.points[earlier].revealed()
            if previous is not None:
                return previous
        return []

    @model_validator(mode="after")
    def consistent(self) -> Scene:
        blocks = [name for name in ("table", "code", "grid") if getattr(self, name) is not None]
        if len(blocks) > 1:
            raise ValueError(f"scene '{self.title}' mixes {blocks}; use one of table/code/grid per scene")
        if self.slide and self.image:
            raise ValueError(f"scene '{self.title}' has both slide and image")
        target = self.reveal_target()
        for i, point in enumerate(self.points, start=1):
            revealed = point.revealed()
            if revealed is None:
                continue
            if not target:
                raise ValueError(f"scene '{self.title}' point {i} uses reveal but has no table/code/grid")
            for value in revealed:
                if not 0 <= value <= target[1]:
                    raise ValueError(f"scene '{self.title}' point {i}: reveal {value} is not a {target[0]} "
                                     f"(valid: 0..{target[1]})")
        has_bullets = any(p.text for p in self.points)
        has_reveals = any(p.reveal is not None for p in self.points)
        if self.table and not has_bullets and not has_reveals and len(self.points) != len(self.table.rows):
            raise ValueError(f"scene '{self.title}': {len(self.points)} narration segments for "
                             f"{len(self.table.rows)} table rows; make them equal or set reveal")
        if self.code and not has_reveals:
            raise ValueError(f"scene '{self.title}': code needs reveal on at least one point")
        if self.table and has_reveals:
            shown = max((max(r) for p in self.points if (r := p.revealed())), default=0)
            if shown < len(self.table.rows):
                raise ValueError(f"scene '{self.title}': table rows after {shown} are never revealed")
        return self


class Script(Strict):
    title: str = Field(min_length=1)
    scenes: list[Scene] = Field(min_length=1)


def load_script(chapter: int) -> Script:
    path = SCRIPTS / f"ch{chapter:02d}.json"
    return Script.model_validate(json.loads(path.read_text(encoding="utf-8")))


_page_counts: dict[int, int] = {}


def slide_page_count(chapter: int) -> int:
    if chapter not in _page_counts:
        with pymupdf.open(SITE / "references" / SLIDE_FILES[chapter]) as doc:
            _page_counts[chapter] = doc.page_count
    return _page_counts[chapter]


DIGIT_DECIMAL = re.compile(r"\d[.,]\d")


def check_assets(chapter: int, script: Script) -> list[str]:
    """Problems that the schema cannot see: missing files, bad page numbers, TTS-unfriendly text."""
    problems: list[str] = []
    for scene in script.scenes:
        where = f"ch{chapter:02d} '{scene.title}'"
        if scene.slide and scene.slide > slide_page_count(chapter):
            problems.append(f"{where}: slide page {scene.slide} > {slide_page_count(chapter)} pages")
        if scene.image:
            target = (SITE / scene.image).resolve()
            if (SITE / "media").resolve() not in target.parents:
                problems.append(f"{where}: image '{scene.image}' is not inside media/")
            elif not target.is_file():
                problems.append(f"{where}: image '{scene.image}' does not exist")
        for i, point in enumerate(scene.points, start=1):
            if DIGIT_DECIMAL.search(point.say):
                problems.append(f"{where} point {i}: write decimals in words for TTS: "
                                f"'{DIGIT_DECIMAL.search(point.say).group()}'")
            if "$" in point.say or "\\" in point.say:
                problems.append(f"{where} point {i}: narration contains LaTeX")
    return problems
