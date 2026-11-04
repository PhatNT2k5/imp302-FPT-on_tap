"""Merge slide-based bonus questions into data.js (idempotent: replaces previous bonus items)."""
import collections
import hashlib
import io
import json
import random
import re
import sys
from pathlib import Path

import pymupdf

SCRATCH, SITE = Path(sys.argv[1]), Path(sys.argv[2])
FILES = {1: "01-1.-Basic-Gray-Level-Image-Processing", 2: "02-2.-Image-and-Video-Processing",
         3: "03-3.-Image-Degradation-Restoration-and-Resconstruction", 4: "04-4.-Image-and-Video-Analysis",
         5: "05-5.-Image-compression", 6: "06-6.-Video-compression", 7: "07-7.-Image-and-Video-Acquisition",
         8: "08-8.-Image-and-Video-Rendering-and-Assessment-1-", 9: "10-9.-Image-and-Video-segmentation",
         10: "11-10.-Feature-extraction", 11: "12-11.-Object-detection", 12: "13-12.-Image-pattern-classification"}
STOP = set("the of a an to in and or for is are be by what which how does do on from as at it its this that with image images".split())


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 2}


rows = [row for f in "abcd" for row in json.loads((SCRATCH / f"bonus_{f}.json").read_text(encoding="utf-8"))]
path = SITE / "data.js"
raw = path.read_text(encoding="utf-8")
pre, body, suf = raw[: raw.index("{")], raw[raw.index("{"): raw.rindex("}") + 1], raw[raw.rindex("}") + 1:]
data = json.loads(body)
items = [r for r in data["items"] if r.get("sourceSet") != "bonus"]
existing = [(r["id"], words(r["question"] + " " + r["answer"])) for r in items]
page_counts = {c: pymupdf.open(SITE / "references" / f"{f}.pdf").page_count for c, f in FILES.items()}

next_id = max(r["id"] for r in items) + 1
added, similar = [], []
seen_questions = set()
for ch, page, question, options, correct, explanation in rows:
    assert 1 <= page <= page_counts[ch], (ch, page, question)
    assert len(options) == 4 and len(set(options)) == 4 and 0 <= correct < 4, question
    assert question not in seen_questions, question
    seen_questions.add(question)
    qa = words(question + " " + options[correct])
    score, other = max(((len(qa & w) / max(1, len(qa | w)), i) for i, w in existing), key=lambda x: x[0])
    if score >= 0.45:
        similar.append((round(score, 2), other, question))
    rng = random.Random(hashlib.sha1(question.encode()).hexdigest())
    order = list(range(4))
    rng.shuffle(order)
    opts = [options[i] for i in order]
    ok = order.index(correct)
    item = {"id": next_id, "type": "quiz", "sourceSet": "bonus", "sourceName": "Câu bổ sung soạn từ slide",
            "question": question, "options": opts, "correct": ok, "answer": opts[ok], "score": 1.0,
            "page": page, "pages": [page], "chapter": ch, "explanation": explanation, "note": "",
            "answerBasis": f"Câu bổ sung · đáp án theo slide chương {ch}, trang {page}.",
            "references": [{"label": f"{FILES[ch][3:]} · trang PDF {page}", "url": f"references/{FILES[ch]}.pdf#page={page}"}],
            "verified": True}
    item["contentSignature"] = hashlib.sha1(json.dumps([question, opts, ok], ensure_ascii=False).encode()).hexdigest()[:16]
    added.append(item)
    next_id += 1

data["items"] = items + added
data["meta"]["bonusCount"] = len(added)
data["meta"]["quizCount"] = sum(r["type"] == "quiz" for r in data["items"])
path.write_text(pre + json.dumps(data, ensure_ascii=False) + suf, encoding="utf-8")
print("added", len(added), "ids", added[0]["id"], "-", added[-1]["id"])
print("answer positions", dict(collections.Counter(r["correct"] for r in added)))
print("quiz per chapter now", sorted(collections.Counter(r["chapter"] for r in data["items"] if r["type"] == "quiz").items()))
for s in similar:
    print("SIMILAR", s)
