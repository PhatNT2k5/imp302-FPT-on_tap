"""Pydantic models and validation for chapter lecture scripts (scripts/chNN.json).

Two script shapes are supported:
  - chapter script (old): {"title", "scenes": [...]} -> one long video per chapter.
  - story script (new):   {"title", "example", "stories": [{"id", "title", "kind", "scenes"}]}
    -> one short video per story (chapter intro, one per method, summary).

A scene has points; each point is one narration segment (`say`) plus what changes on
screen while it is spoken:
  - `text`   : a bullet that appears with this point (optional)
  - `reveal` : which table rows / code lines / grids / visual steps are highlighted (optional)
  - `ask`    : a "guess first" moment: badge on screen + a pause before the answer
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
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

OldKicker = Literal["Recap", "Intuition", "Formula", "Worked example", "Algorithm", "Compare", "Exam traps", "Summary"]
# Story beats in the order a method story tells them (README "Story template").
# "Cách làm" and "Công thức" share a rank: a formula may sit between worked steps.
BEAT_RANK = {"Vấn đề": 0, "Cách cũ": 1, "Ý tưởng": 2, "Cách làm": 3, "Công thức": 3, "So sánh": 4,
             "Ứng dụng": 5, "Hạn chế": 6, "Bẫy thi": 7}
METHOD_REQUIRED = ("Vấn đề", "Cách cũ", "Ý tưởng", "Cách làm", "So sánh", "Ứng dụng", "Hạn chế", "Bẫy thi")
EXTRA_REQUIRED = ("Vấn đề", "Ý tưởng", "Bẫy thi")
Beat = Literal["Mở đầu", "Vấn đề", "Cách cũ", "Ý tưởng", "Cách làm", "Công thức", "So sánh", "Ứng dụng", "Hạn chế",
               "Bẫy thi", "Tổng kết"]
Kicker = OldKicker | Beat
Style = Literal["accent", "warn", "dim", "cut"]
Cell = str | int | float
CHARS_PER_SECOND = 14  # measured on rendered chapters: ~0.072 s of speech per character at RATE -4%
STORY_MINUTES = {"intro": (0.5, 2.5), "method": (1.5, 6.5), "extra": (1.0, 4.5), "summary": (0.8, 3.5)}


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


# ---------- staged visuals: every element appears at a reveal step and may change style later ----------

class Mark(Strict):
    """From reveal step `step` on, draw the element with `style` (the latest mark reached wins)."""
    step: int = Field(ge=0)
    style: Style


class Staged(Strict):
    step: int = Field(default=0, ge=0)  # appears at this reveal step (0 = from the start)
    marks: list[Mark] = []

    def last_step(self) -> int:
        return max([self.step, *(m.step for m in self.marks)])


class Node(Staged):
    id: str = Field(min_length=1)
    label: str = ""
    x: float
    y: float
    shape: Literal["circle", "box", "dot"] = "circle"
    note: str | None = None  # small text under the node, e.g. a probability


class Edge(Staged):
    a: str
    b: str
    label: str | None = None


class Graph(Strict):
    """Nodes at (x, y) in any units (y grows downward) joined by edges. Also used for trees and scatter plots."""
    nodes: list[Node] = Field(min_length=1)
    edges: list[Edge] = []
    arrows: bool = False
    caption: str | None = None

    @model_validator(mode="after")
    def edges_known(self) -> Graph:
        ids = [n.id for n in self.nodes]
        if len(set(ids)) != len(ids):
            raise ValueError("graph node ids must be unique")
        for e in self.edges:
            if e.a not in ids or e.b not in ids:
                raise ValueError(f"edge {e.a}-{e.b} uses an unknown node")
        return self

    def steps(self) -> int:
        return max(item.last_step() for item in [*self.nodes, *self.edges])


class Bar(Staged):
    label: str
    value: float = Field(ge=0)


class Line(Staged):
    at: float  # in bar units: 0 = left edge of the first bar, len(bars) = right edge of the last
    label: str


class Band(Staged):
    start: float  # in bar units, like Line.at
    end: float
    label: str | None = None


class Histogram(Strict):
    bars: list[Bar] = Field(min_length=1)
    lines: list[Line] = []
    bands: list[Band] = []
    caption: str | None = None

    def steps(self) -> int:
        return max(item.last_step() for item in [*self.bars, *self.lines, *self.bands])


class Interval(Staged):
    """One row of arithmetic coding: [low, high) split into named parts; `pick` is the part kept for the next row."""
    low: float
    high: float
    parts: list[tuple[str, float, float]] = Field(min_length=1)
    pick: str | None = None

    @model_validator(mode="after")
    def pick_known(self) -> Interval:
        if self.pick and self.pick not in [p[0] for p in self.parts]:
            raise ValueError(f"interval pick '{self.pick}' is not one of its parts")
        return self


class Intervals(Strict):
    rows: list[Interval] = Field(min_length=1)
    caption: str | None = None

    def steps(self) -> int:
        return max(r.last_step() for r in self.rows)


class Panel(Strict):
    label: str
    grid: Grid | None = None
    histogram: Histogram | None = None
    image: str | None = None

    @model_validator(mode="after")
    def one_body(self) -> Panel:
        if sum(x is not None for x in (self.grid, self.histogram, self.image)) != 1:
            raise ValueError(f"panel '{self.label}' needs exactly one of grid/histogram/image")
        return self


class Compare(Strict):
    """Before -> after. Reveal 1 shows the left panel, reveal 2 adds the arrow and the right panel."""
    left: Panel
    right: Panel
    arrow: str = ""

    def steps(self) -> int:
        return 2


class Chain(Strict):
    """The chapter's chain of methods; `current` (1-based) is highlighted, earlier items are done."""
    items: list[str] = Field(min_length=2)
    current: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def current_inside(self) -> Chain:
        if self.current > len(self.items):
            raise ValueError(f"chain current {self.current} > {len(self.items)} items")
        return self


VISUALS = ("table", "code", "grid", "graph", "histogram", "intervals", "compare", "chain")
STAGED = ("graph", "histogram", "intervals", "compare")


class Point(Strict):
    say: str = Field(min_length=1)
    text: str | None = None
    reveal: int | list[int] | None = None
    ask: bool = False
    pause: float | None = Field(default=None, ge=0, le=6)  # extra silence after the point

    def revealed(self) -> list[int] | None:
        if self.reveal is None:
            return None
        return [self.reveal] if isinstance(self.reveal, int) else list(self.reveal)

    def silence(self) -> float:
        return self.pause if self.pause is not None else (2.0 if self.ask else 0.0)


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
    graph: Graph | None = None
    histogram: Histogram | None = None
    intervals: Intervals | None = None
    compare: Compare | None = None
    chain: Chain | None = None

    def grids(self) -> list[Grid]:
        if self.grid is None:
            return []
        return [self.grid] if isinstance(self.grid, Grid) else self.grid

    def visual(self) -> str | None:
        return next((name for name in VISUALS if getattr(self, name) is not None), None)

    def reveal_target(self) -> tuple[str, int] | None:
        """What `reveal` indexes in this scene, and how many items it has."""
        if self.table:
            return "table row", len(self.table.rows)
        if self.code:
            return "code line", len(self.code.lines)
        if self.grid is not None:
            return "grid", len(self.grids())
        for name in STAGED:
            if getattr(self, name) is not None:
                return f"{name} step", getattr(self, name).steps()
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

    def reach_at(self, index: int) -> int:
        """Highest item revealed so far: earlier rows / steps stay on screen."""
        return max((max(self.reveal_at(i), default=0) for i in range(index + 1)), default=0)

    @model_validator(mode="after")
    def consistent(self) -> Scene:
        blocks = [name for name in VISUALS if getattr(self, name) is not None]
        if len(blocks) > 1:
            raise ValueError(f"scene '{self.title}' mixes {blocks}; use one visual per scene")
        if self.slide and self.image:
            raise ValueError(f"scene '{self.title}' has both slide and image")
        if (self.slide or self.image) and blocks and blocks[0] in (*STAGED, "chain"):
            raise ValueError(f"scene '{self.title}': a {blocks[0]} needs the full width; drop slide/image")
        target = self.reveal_target()
        for i, point in enumerate(self.points, start=1):
            revealed = point.revealed()
            if revealed is None:
                continue
            if not target:
                raise ValueError(f"scene '{self.title}' point {i} uses reveal but has no table/code/grid/visual")
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
        if target and target[0].endswith(" step") and target[1] > 0:
            shown = max((max(r) for p in self.points if (r := p.revealed())), default=0)
            if shown < target[1]:
                raise ValueError(f"scene '{self.title}': {target[0]}s after {shown} are never revealed")
        return self


class Script(Strict):
    title: str = Field(min_length=1)
    scenes: list[Scene] = Field(min_length=1)


class Story(Strict):
    id: str = Field(pattern=r"^[a-z0-9-]+$")
    title: str = Field(min_length=1)
    kind: Literal["intro", "method", "extra", "summary"]
    scenes: list[Scene] = Field(min_length=1)

    def seconds(self) -> float:
        """Rough spoken length, used to keep stories short before paying for TTS."""
        points = [p for s in self.scenes for p in s.points]
        return sum(len(p.say) for p in points) / CHARS_PER_SECOND + sum(0.45 + p.silence() for p in points)


class StoryScript(Strict):
    title: str = Field(min_length=1)
    example: str = Field(min_length=1)  # the running example every story comes back to
    stories: list[Story] = Field(min_length=2)

    @model_validator(mode="after")
    def beats_in_order(self) -> StoryScript:
        ids = [s.id for s in self.stories]
        if len(set(ids)) != len(ids):
            raise ValueError("story ids must be unique")
        first_method = next((s.id for s in self.stories if s.kind == "method"), None)
        for story in self.stories:
            beats = [scene.kicker for scene in story.scenes]
            if story.kind in ("method", "extra"):
                unknown = [b for b in beats if b not in BEAT_RANK]
                if unknown:
                    raise ValueError(f"story '{story.id}': kicker {unknown[0]!r} is not a story beat")
                ranks = [BEAT_RANK[b] for b in beats]
                if ranks != sorted(ranks):
                    raise ValueError(f"story '{story.id}': beats out of order: {beats}")
                required = METHOD_REQUIRED if story.kind == "method" else EXTRA_REQUIRED
                missing = [b for b in required if b not in beats and not (b == "Cách cũ" and story.id == first_method)]
                if missing:
                    raise ValueError(f"story '{story.id}': missing beats {missing}")
            elif story.kind == "intro" and beats[0] != "Mở đầu":
                raise ValueError(f"story '{story.id}': an intro starts with kicker 'Mở đầu'")
            elif story.kind == "summary" and "Tổng kết" not in beats:
                raise ValueError(f"story '{story.id}': a summary needs a 'Tổng kết' scene")
        return self


def script_path(chapter: int) -> Path:
    return SCRIPTS / f"ch{chapter:02d}.json"


def load_script(chapter: int) -> Script | StoryScript:
    raw = json.loads(script_path(chapter).read_text(encoding="utf-8"))
    return StoryScript.model_validate(raw) if "stories" in raw else Script.model_validate(raw)


@dataclass
class Unit:
    """One rendered video: a whole old-style chapter, or one story of a story script."""
    chapter: int
    chapter_title: str
    stem: str  # output path under media/lectures without extension
    title: str
    kind: str  # "lecture" for old chapter videos, else the story kind
    number: int  # position among the chapter's videos (0 = intro)
    total: int
    scenes: list[Scene]
    agenda: list[str]


def load_units(chapter: int) -> list[Unit]:
    from slides import latex_to_unicode  # local import: slides imports this module

    script = load_script(chapter)
    if isinstance(script, Script):
        agenda = [latex_to_unicode(s.title) for s in script.scenes if s.kind != "intro"]
        return [Unit(chapter, script.title, f"ch{chapter:02d}", script.title, "lecture", 0, 1, script.scenes, agenda)]
    agenda = [s.title for s in script.stories if s.kind in ("method", "extra")]
    total = len(script.stories)
    return [Unit(chapter, script.title, f"ch{chapter:02d}/{n:02d}-{s.id}", s.title, s.kind, n, total, s.scenes, agenda)
            for n, s in enumerate(script.stories)]


_page_counts: dict[int, int] = {}


def slide_page_count(chapter: int) -> int:
    if chapter not in _page_counts:
        with pymupdf.open(SITE / "references" / SLIDE_FILES[chapter]) as doc:
            _page_counts[chapter] = doc.page_count
    return _page_counts[chapter]


DIGIT_DECIMAL = re.compile(r"\d[.,]\d")


def _image_problem(where: str, image: str) -> str | None:
    target = (SITE / image).resolve()
    if (SITE / "media").resolve() not in target.parents:
        return f"{where}: image '{image}' is not inside media/"
    if not target.is_file():
        return f"{where}: image '{image}' does not exist"
    return None


def check_assets(chapter: int, script: Script | StoryScript) -> list[str]:
    """Problems that the schema cannot see: missing files, bad page numbers, TTS-unfriendly text, length."""
    problems: list[str] = []
    groups = [("", script.scenes)] if isinstance(script, Script) else [(f"{s.id}/", s.scenes) for s in script.stories]
    for prefix, scenes in groups:
        for scene in scenes:
            where = f"ch{chapter:02d} {prefix}'{scene.title}'"
            if scene.slide and scene.slide > slide_page_count(chapter):
                problems.append(f"{where}: slide page {scene.slide} > {slide_page_count(chapter)} pages")
            images = [scene.image] if scene.image else []
            if scene.compare:
                images += [p.image for p in (scene.compare.left, scene.compare.right) if p.image]
            problems += [p for img in images if (p := _image_problem(where, img))]
            for i, point in enumerate(scene.points, start=1):
                if DIGIT_DECIMAL.search(point.say):
                    problems.append(f"{where} point {i}: write decimals in words for TTS: "
                                    f"'{DIGIT_DECIMAL.search(point.say).group()}'")
                if "$" in point.say or "\\" in point.say:
                    problems.append(f"{where} point {i}: narration contains LaTeX")
    if isinstance(script, StoryScript):
        for story in script.stories:
            low, high = STORY_MINUTES[story.kind]
            minutes = story.seconds() / 60
            if not low <= minutes <= high:
                problems.append(f"ch{chapter:02d} {story.id}: ~{minutes:.1f} min, a {story.kind} story should be "
                                f"{low}-{high} min")
    return problems
