"""Turn lecture units (scripts/chNN.json) into frame states and draw them with slide_template.html in a headless browser."""
from __future__ import annotations

import re
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator

import pymupdf
from playwright.async_api import Page, async_playwright

from script_model import ROOT, SITE, SLIDE_FILES, Grid, Histogram, Panel, Scene, Staged, Unit

TEMPLATE = ROOT / "slide_template.html"
SLIDE_CACHE = ROOT / "cache" / "slides"
BROWSER_CHANNELS = ("msedge", "chrome")


@dataclass
class Frame:
    scene_index: int
    point_index: int
    state: dict


def slide_png(chapter: int, page: int) -> Path:
    """Rasterise one page of the original lecture PDF (cached on disk)."""
    SLIDE_CACHE.mkdir(parents=True, exist_ok=True)
    out = SLIDE_CACHE / f"ch{chapter:02d}-p{page:02d}.png"
    if not out.exists():
        with pymupdf.open(SITE / "references" / SLIDE_FILES[chapter]) as doc:
            doc[page - 1].get_pixmap(dpi=130).save(out)
    return out


def grid_state(grid: Grid, visible: bool = True, current: bool = False) -> dict:
    marks = {f"{r},{c}": name for name in ("dim", "accent", "warn") for r, c in getattr(grid, name)}
    return {"label": grid.label, "cells": [[str(c) for c in row] for row in grid.cells], "marks": marks,
            "visible": visible, "current": current}


def staged(item: Staged, reach: int, shown: list[int]) -> dict:
    """Serialise one visual element with what the current frame shows of it."""
    data = item.model_dump(exclude={"marks", "step"})
    style = next((m.style for m in sorted(item.marks, key=lambda m: m.step, reverse=True) if m.step <= reach), None)
    data.update(visible=item.step <= reach, current=item.step > 0 and item.step in shown, style=style)
    return data


def histogram_state(h: Histogram, reach: int, shown: list[int]) -> dict:
    return {"bars": [staged(b, reach, shown) for b in h.bars], "lines": [staged(x, reach, shown) for x in h.lines],
            "bands": [staged(b, reach, shown) for b in h.bands], "caption": h.caption}


def panel_state(panel: Panel) -> dict:
    if panel.grid:
        return {"label": panel.label, "grid": grid_state(panel.grid)}
    if panel.histogram:
        return {"label": panel.label, "histogram": histogram_state(panel.histogram, 10**6, [])}
    return {"label": panel.label, "image": (SITE / panel.image).resolve().as_uri()}


def visual_state(scene: Scene, reach: int, shown: list[int]) -> dict | None:
    if scene.graph:
        g = scene.graph
        return {"type": "graph", "arrows": g.arrows, "caption": g.caption,
                "nodes": [staged(n, reach, shown) for n in g.nodes], "edges": [staged(e, reach, shown) for e in g.edges]}
    if scene.histogram:
        return {"type": "histogram", **histogram_state(scene.histogram, reach, shown)}
    if scene.intervals:
        return {"type": "intervals", "caption": scene.intervals.caption,
                "rows": [staged(r, reach, shown) for r in scene.intervals.rows]}
    if scene.compare:
        c = scene.compare
        return {"type": "compare", "arrow": c.arrow, "left": panel_state(c.left), "right": panel_state(c.right),
                "showLeft": reach >= 1, "showRight": reach >= 2}
    if scene.chain:
        return {"type": "chain", "items": scene.chain.items, "current": scene.chain.current}
    return None


def frame_state(unit: Unit, scene_index: int, point_index: int) -> dict:
    scene: Scene = unit.scenes[scene_index]
    point = scene.points[point_index]
    shown = scene.reveal_at(point_index)
    reach = scene.reach_at(point_index)

    bullets, last_bullet = [], -1
    for i, p in enumerate(scene.points):
        if p.text:
            bullets.append({"text": p.text, "visible": i <= point_index, "current": False})
            if i <= point_index:
                last_bullet = len(bullets) - 1
    if last_bullet >= 0:
        bullets[last_bullet]["current"] = True

    media = None
    if scene.slide:
        media = {"src": slide_png(unit.chapter, scene.slide).as_uri(), "caption": f"Slide gốc · trang {scene.slide}"}
    elif scene.image:
        media = {"src": (SITE / scene.image).resolve().as_uri(), "caption": scene.image}

    table = None
    if scene.table:
        table = {"headers": scene.table.headers,
                 "rows": [{"cells": [str(c) for c in row], "visible": n <= reach, "current": n in shown}
                          for n, row in enumerate(scene.table.rows, start=1)]}
    code = None
    if scene.code:
        code = [{"text": line, "current": n in shown} for n, line in enumerate(scene.code.lines, start=1)]
    only_grid = len(scene.grids()) == 1
    grids = [grid_state(g, only_grid or n <= reach, n in shown) for n, g in enumerate(scene.grids(), start=1)]

    story = unit.kind != "lecture"
    label = f"VIDEO {unit.number:02d}/{unit.total - 1:02d}" if story and unit.number else ""
    points_total = len(scene.points)
    return {
        "chapter": unit.chapter, "chapterTitle": unit.chapter_title, "unitLabel": label,
        "intro": scene.kind == "intro", "agenda": scene.agenda or unit.agenda, "title": scene.title,
        "kicker": scene.kicker, "story": story, "ask": point.ask,
        "media": media, "wide": bool(scene.table or scene.code or scene.grid or scene.formula),
        "formula": scene.formula, "bullets": bullets, "table": table, "code": code, "grids": grids,
        "visual": visual_state(scene, reach, shown),
        "sceneIndex": scene_index, "sceneCount": len(unit.scenes),
        "progress": (scene_index + (point_index + 1) / points_total) / len(unit.scenes),
    }


def unit_frames(unit: Unit) -> list[Frame]:
    return [Frame(si, pi, frame_state(unit, si, pi))
            for si, scene in enumerate(unit.scenes) for pi in range(len(scene.points))]


@asynccontextmanager
async def slide_page() -> AsyncIterator[Page]:
    """A 1280x720 page with the slide template loaded, using an installed Edge or Chrome."""
    async with async_playwright() as pw:
        browser, errors = None, []
        for channel in BROWSER_CHANNELS:
            try:
                browser = await pw.chromium.launch(channel=channel)
                break
            except Exception as exc:  # channel not installed: try the next one
                errors.append(f"{channel}: {exc}")
        if browser is None:
            raise RuntimeError("No Edge or Chrome found for rendering slides:\n" + "\n".join(errors))
        try:
            page = await browser.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
            page.on("pageerror", lambda exc: print(f"slide page error: {exc}"))
            await page.goto(TEMPLATE.as_uri())
            yield page
        finally:
            await browser.close()


async def draw(page: Page, frame: Frame, png: Path | None = None) -> list[str]:
    """Render one frame; returns its overflow problems and optionally saves a screenshot."""
    result = await page.evaluate("state => window.renderState(state)", frame.state)
    if png:
        await page.screenshot(path=str(png))
    return result["problems"]


# ---------- plain-text titles for the video outline ----------

SYMBOLS = {
    r"\epsilon": "ε", r"\varepsilon": "ε", r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ",
    r"\Delta": "Δ", r"\theta": "θ", r"\lambda": "λ", r"\mu": "μ", r"\pi": "π", r"\rho": "ρ", r"\sigma": "σ",
    r"\Sigma": "Σ", r"\phi": "φ", r"\omega": "ω", r"\eta": "η", r"\times": "×", r"\cdot": "·", r"\to": "→",
    r"\rightarrow": "→", r"\leftarrow": "←", r"\le": "≤", r"\leq": "≤", r"\ge": "≥", r"\geq": "≥", r"\neq": "≠",
    r"\approx": "≈", r"\sum": "Σ", r"\infty": "∞", r"\pm": "±", r"\in": "∈", r"\cap": "∩", r"\cup": "∪",
    r"\mid": "|", r"\ldots": "…", r"\dots": "…", r"\,": " ", r"\;": " ", r"\ ": " ", r"\!": "",
}
SUPERSCRIPT = str.maketrans("0123456789+-=()n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ")
SUBSCRIPT = str.maketrans("0123456789+-=()aeoxhklmnpst", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₕₖₗₘₙₚₛₜ")


def _script_text(match: re.Match, table: dict, fallback: str) -> str:
    body = match.group(1) or match.group(2)
    converted = body.translate(table)
    unchanged = [ch for ch, out in zip(body, converted) if ch == out and not ch.isspace()]
    return converted if not unchanged else f"{fallback}{body}" if len(body) == 1 else f"{fallback}({body})"


def _math_to_unicode(tex: str) -> str:
    tex = re.sub(r"\\(?:text|mathrm|mathbf|mathit|operatorname)\{([^{}]*)\}", r"\1", tex)
    tex = re.sub(r"\\(?:hat|bar|tilde|vec)\{([^{}]*)\}", r"\1", tex)
    for _ in range(3):  # nested fractions / roots
        tex = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", tex)
        tex = re.sub(r"\\sqrt\{([^{}]*)\}", r"√(\1)", tex)
    for command in sorted(SYMBOLS, key=len, reverse=True):
        tex = re.sub(re.escape(command) + r"(?![A-Za-z])" if command[-1].isalpha() else re.escape(command),
                     SYMBOLS[command], tex)
    tex = re.sub(r"\^(?:\{([^{}]*)\}|(.))", lambda m: _script_text(m, SUPERSCRIPT, "^"), tex)
    tex = re.sub(r"_(?:\{([^{}]*)\}|(.))", lambda m: _script_text(m, SUBSCRIPT, "_"), tex)
    tex = re.sub(r"\\([A-Za-z]+)", r"\1", tex)  # unknown command: keep its name, drop the backslash
    return tex.replace("{", "").replace("}", "").replace("\\", "")


def latex_to_unicode(text: str) -> str:
    """Replace every $...$ span with readable Unicode, e.g. '$\\epsilon$-greedy' -> 'ε-greedy'."""
    return re.sub(r"\$\$?(.+?)\$\$?", lambda m: _math_to_unicode(m.group(1)), text)
