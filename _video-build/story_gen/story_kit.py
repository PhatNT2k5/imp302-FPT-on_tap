"""Shared helpers for the chapter story-script generators (gen_chNN.py)."""
import json
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent


def P(say, text=None, reveal=None, ask=False, pause=None):
    point = {"say": say}
    if text:
        point["text"] = text
    if reveal is not None:
        point["reveal"] = reveal
    if ask:
        point["ask"] = True
    if pause is not None:
        point["pause"] = pause
    return point


def S(kicker, title, points, **extra):
    return {"kicker": kicker, "title": title, "points": points, **extra}


def traps(rows, says, title="Bẫy thi"):
    return S("Bẫy thi", title, [P(s) for s in says], table={"headers": ["Câu hỏi", "Đáp án"], "rows": rows})


def chain(items, current):
    return {"items": items, "current": current}


def limit(title, points, items, next_index):
    return S("Hạn chế", title, points, chain=chain(items, next_index))


def pipeline(labels, steps, vertical=True):
    nodes = [{"id": f"n{i}", "label": label, "x": 0 if vertical else i, "y": i if vertical else 0, "shape": "box",
              "step": step} for i, (label, step) in enumerate(zip(labels, steps))]
    edges = [{"a": f"n{i}", "b": f"n{i + 1}", "step": steps[i + 1]} for i in range(len(labels) - 1)]
    return {"nodes": nodes, "edges": edges, "arrows": True}


def story(sid, title, kind, scenes):
    return {"id": sid, "title": title, "kind": kind, "scenes": scenes}


def intro(sid, title, hello, example_points, items, road_points):
    """Standard chapter intro: the running example, then the chain of methods."""
    return story(sid, title, "intro", [
        S("Mở đầu", hello, example_points),
        S("Mở đầu", "Lộ trình của chương", road_points, chain=chain(items, 0)),
    ])


def write(chapter, title, example, stories, map_rows=None, map_notes=""):
    out = BUILD / "scripts" / f"ch{chapter:02d}.json"
    script = {"title": title, "example": example, "stories": stories}
    out.write_text(json.dumps(script, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out.name}: {len(stories)} stories")
    if map_rows:
        lines = [f"# Bản đồ câu chuyện – Chương {chapter}: {title}", "", f"**Ví dụ xuyên suốt:** {example}", "",
                 "| # | Video | Slide | Vấn đề | Cách cũ & chỗ hụt | Ý tưởng cốt lõi | Hạn chế → dẫn sang |",
                 "|---|---|---|---|---|---|---|"]
        for n, row in enumerate(map_rows):
            lines.append(f"| {n:02d} | " + " | ".join(row) + " |")
        if map_notes:
            lines += ["", map_notes]
        path = BUILD / "story_maps" / f"ch{chapter:02d}.md"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"wrote {path.name}")
