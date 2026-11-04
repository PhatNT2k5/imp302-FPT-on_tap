"""Render narrated Vietnamese lecture videos from chapter scripts.

Usage: python -I build_lecture.py 1 2 3   (no args = all chapters with a script)

Each scripts/chNN.json holds scenes; each scene has points, and each point is one
bullet on screen plus the narration spoken while that bullet is highlighted.
"""
import asyncio
import hashlib
import json
import re
import subprocess
import sys
import wave
from dataclasses import dataclass, field
from pathlib import Path

import edge_tts
import imageio_ffmpeg
import pymupdf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SITE = ROOT.parent
SCRIPTS = ROOT / "scripts"
CACHE = ROOT / "cache"
OUT_DIR = SITE / "media" / "lectures"
MANIFEST = SITE / "lecture-data.js"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

VOICE = "vi-VN-HoaiMyNeural"
RATE = "-4%"
SAMPLE_RATE = 24000
POINT_GAP = 0.45  # seconds of silence after each point
SCENE_GAP = 0.9  # extra silence when a scene ends

W, H = 1280, 720
BG = "#111c18"
SURFACE = "#1b2a22"
INK = "#e4eee1"
MUTED = "#8fa392"
ACCENT = "#a9c995"
ORANGE = "#edb78e"
LINE = "#35463a"

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


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    files = {"regular": "segoeui.ttf", "semibold": "seguisb.ttf", "bold": "segoeuib.ttf"}
    return ImageFont.truetype(f"C:/Windows/Fonts/{files[weight]}", size)


# ---------- text-to-speech ----------

@dataclass
class Cue:
    start: float
    end: float
    text: str


@dataclass
class Speech:
    wav: Path
    duration: float
    cues: list[Cue] = field(default_factory=list)


_tts_slots = asyncio.Semaphore(2)  # the TTS service throttles bursts of parallel requests


async def synthesize(text: str) -> Speech:
    async with _tts_slots:
        return await _synthesize(text)


async def _request(text: str, attempts: int) -> tuple[bytes, list[dict]]:
    for attempt in range(attempts):
        try:
            audio = bytearray()
            cues: list[dict] = []
            stream = edge_tts.Communicate(text, VOICE, rate=RATE, boundary="SentenceBoundary").stream()
            async for chunk in stream:
                if chunk["type"] == "audio":
                    audio.extend(chunk["data"])
                elif chunk["type"] == "SentenceBoundary":
                    start = chunk["offset"] / 1e7
                    cues.append({"start": start, "end": start + chunk["duration"] / 1e7, "text": chunk["text"]})
            if not audio:
                raise RuntimeError("empty audio")
            return bytes(audio), cues
        except Exception as exc:  # the service intermittently returns no audio; retry with backoff
            if attempt == attempts - 1:
                raise RuntimeError(f"TTS failed for: {text[:60]}...") from exc
            await asyncio.sleep(min(1 + attempt, 6))
    raise AssertionError("unreachable")


def mp3_to_pcm(audio: bytes, scratch: Path) -> bytes:
    scratch.write_bytes(audio)
    wav_path = scratch.with_suffix(".part.wav")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(scratch), "-ac", "1", "-ar", str(SAMPLE_RATE),
                    "-sample_fmt", "s16", str(wav_path)], check=True)
    with wave.open(str(wav_path)) as w:
        pcm = w.readframes(w.getnframes())
    wav_path.unlink()
    return pcm


async def _synthesize(text: str) -> Speech:
    key = hashlib.sha1(f"{VOICE}|{RATE}|{text}".encode()).hexdigest()[:16]
    wav, meta = CACHE / f"{key}.wav", CACHE / f"{key}.json"
    if not (wav.exists() and meta.exists()):
        try:
            audio, cues = await _request(text, attempts=8)
            pcm = mp3_to_pcm(audio, CACHE / f"{key}.mp3")
        except RuntimeError:
            # Some long passages keep failing as a whole but succeed sentence by sentence.
            pcm, cues = b"", []
            for part in re.split(r"(?<=[.!?:])\s+", text.strip()):
                part_audio, _ = await _request(part, attempts=30)
                start = len(pcm) / 2 / SAMPLE_RATE
                pcm += mp3_to_pcm(part_audio, CACHE / f"{key}.mp3") + silence(int(0.12 * SAMPLE_RATE))
                cues.append({"start": start, "end": len(pcm) / 2 / SAMPLE_RATE, "text": part})
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SAMPLE_RATE)
            w.writeframes(pcm)
        meta.write_text(json.dumps(cues, ensure_ascii=False), encoding="utf-8")
    with wave.open(str(wav)) as w:
        duration = w.getnframes() / w.getframerate()
    cues = [Cue(**c) for c in json.loads(meta.read_text(encoding="utf-8"))]
    return Speech(wav, duration, cues)


# ---------- frame rendering ----------

def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    line = ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


_slide_cache: dict[tuple[int, int], Image.Image] = {}


def slide_image(chapter: int, page: int, box: tuple[int, int]) -> Image.Image:
    key = (chapter, page)
    if key not in _slide_cache:
        with pymupdf.open(SITE / "references" / SLIDE_FILES[chapter]) as doc:
            pix = doc[page - 1].get_pixmap(dpi=150)
            _slide_cache[key] = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    img = _slide_cache[key].copy()
    img.thumbnail(box, Image.LANCZOS)
    return img


def draw_bullets(draw: ImageDraw.ImageDraw, points: list[str], current: int, x: int, y: int, width: int,
                 max_bottom: int, size: int) -> None:
    for fsize in (size, size - 2, size - 4, size - 6):
        fnt = font(fsize)
        blocks = [wrap(draw, p, fnt, width - 26) for p in points[: current + 1]]
        line_h = int(fsize * 1.42)
        total = sum(len(b) * line_h + 18 for b in blocks)
        if y + total <= max_bottom:
            break
    first = 0
    while y + sum(len(b) * line_h + 18 for b in blocks[first:]) > max_bottom and first < current:
        first += 1  # still too tall at the smallest size: scroll the oldest bullets out
    cy = y
    for i, lines in enumerate(blocks[first:], start=first):
        is_current = i == current
        block_h = len(lines) * line_h
        draw.rounded_rectangle((x, cy + 4, x + 5, cy + block_h - 4), radius=3, fill=ACCENT if is_current else LINE)
        for j, ln in enumerate(lines):
            draw.text((x + 22, cy + j * line_h), ln, font=fnt, fill=INK if is_current else MUTED)
        cy += block_h + 18


def render_frame(chapter: int, chapter_title: str, scene: dict, point_index: int, scene_index: int,
                 scene_count: int) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((48, 26), f"CHƯƠNG {chapter} · {chapter_title.upper()}", font=font(17, "semibold"), fill=ACCENT)
    points = [p["text"] for p in scene["points"]]

    if scene.get("kind") == "intro":
        d.text((48, 120), f"Chương {chapter}", font=font(34, "semibold"), fill=ORANGE)
        d.text((48, 165), chapter_title, font=font(62, "bold"), fill=INK)
        d.text((48, 270), "Hôm nay chúng ta sẽ đi qua:", font=font(22), fill=MUTED)
        agenda_font = font(22)
        for i, item in enumerate(scene["agenda"]):
            col, row = divmod(i, 6)
            d.text((60 + col * 590, 315 + row * 46), f"{i + 1:02d}  {item}", font=agenda_font, fill=INK)
    else:
        title_font = font(36, "bold")
        title_lines = wrap(d, scene["title"], title_font, W - 96)
        if len(title_lines) > 1:
            title_font = font(30, "bold")
            title_lines = wrap(d, scene["title"], title_font, W - 96)[:2]
        for j, ln in enumerate(title_lines):
            d.text((48, 54 + j * 40), ln, font=title_font, fill=INK)
        top = 116 + 40 * (len(title_lines) - 1)
        slide = scene.get("slide")
        if slide:
            card = (40, top + 8, 760, 650)
            d.rounded_rectangle(card, radius=14, fill=SURFACE, outline=LINE)
            simg = slide_image(chapter, slide, (card[2] - card[0] - 24, card[3] - card[1] - 52))
            ox = card[0] + (card[2] - card[0] - simg.width) // 2
            oy = card[1] + 12 + (card[3] - card[1] - 52 - simg.height) // 2
            img.paste(simg, (ox, oy))
            d.text((card[0] + 14, card[3] - 32), f"Slide gốc · trang {slide}", font=font(15), fill=MUTED)
            draw_bullets(d, points, point_index, 790, top + 14, 450, 650, 22)
        else:
            draw_bullets(d, points, point_index, 70, top + 24, W - 140, 650, 27)

    d.rounded_rectangle((48, 676, W - 48, 680), radius=2, fill=LINE)
    done = 48 + int((W - 96) * (scene_index + (point_index + 1) / len(points)) / scene_count)
    d.rounded_rectangle((48, 676, done, 680), radius=2, fill=ACCENT)
    d.text((48, 688), "nhịp học · IMP302", font=font(14), fill=MUTED)
    label = f"Phần {scene_index + 1}/{scene_count}"
    d.text((W - 48 - d.textlength(label, font=font(14)), 688), label, font=font(14), fill=MUTED)
    return img


# ---------- assembly ----------

def vtt_time(t: float) -> str:
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def split_cue(cue: Cue, max_chars: int = 80) -> list[Cue]:
    """Break long sentences at commas into shorter captions, timing each piece by its length."""
    if len(cue.text) <= max_chars:
        return [cue]
    pieces: list[str] = []
    for clause in re.split(r"(?<=,)\s+", cue.text):
        if pieces and len(pieces[-1]) + len(clause) + 1 <= max_chars:
            pieces[-1] += " " + clause
        else:
            pieces.append(clause)
    total = sum(len(p) for p in pieces)
    out, t = [], cue.start
    for p in pieces:
        dt = (cue.end - cue.start) * len(p) / total
        out.append(Cue(t, t + dt, p))
        t += dt
    return out


def silence(frames: int) -> bytes:
    return b"\x00\x00" * frames


async def build_chapter(chapter: int) -> dict:
    spec = json.loads((SCRIPTS / f"ch{chapter:02d}.json").read_text(encoding="utf-8"))
    title = spec["title"]
    scenes = spec["scenes"]
    for scene in scenes:
        if scene.get("kind") == "intro" and "agenda" not in scene:
            scene["agenda"] = [s["title"] for s in scenes if s.get("kind") != "intro"]
    work = CACHE / f"ch{chapter:02d}"
    work.mkdir(parents=True, exist_ok=True)

    speeches = await asyncio.gather(*[synthesize(p["say"]) for s in scenes for p in s["points"]])
    speech_iter = iter(speeches)

    pcm = bytearray()
    t = 0.0
    concat_lines: list[str] = []
    cues: list[Cue] = []
    outline: list[dict] = []
    frame_no = 0
    for si, scene in enumerate(scenes):
        outline.append({"title": scene["title"], "start": round(t, 2)})
        for pi, _point in enumerate(scene["points"]):
            sp = next(speech_iter)
            gap = POINT_GAP + (SCENE_GAP if pi == len(scene["points"]) - 1 else 0)
            with wave.open(str(sp.wav)) as w:
                pcm.extend(w.readframes(w.getnframes()))
            pcm.extend(silence(int(gap * SAMPLE_RATE)))
            cues.extend(piece for c in sp.cues for piece in split_cue(Cue(t + c.start, t + c.end, c.text)))
            frame_path = work / f"f{frame_no:03d}.png"
            render_frame(chapter, title, scene, pi, si, len(scenes)).save(frame_path)
            seg = sp.duration + gap
            concat_lines += [f"file '{frame_path.as_posix()}'", f"duration {seg:.3f}"]
            t += seg
            frame_no += 1
    concat_lines.append(f"file '{(work / f'f{frame_no - 1:03d}.png').as_posix()}'")

    audio_path = work / "audio.wav"
    with wave.open(str(audio_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(bytes(pcm))
    (work / "frames.txt").write_text("\n".join(concat_lines), encoding="utf-8")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = f"ch{chapter:02d}"
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(work / "frames.txt"),
                    "-i", str(audio_path), "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage",
                    "-crf", "26", "-r", "12", "-g", "48", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "80k",
                    "-shortest", "-movflags", "+faststart", str(OUT_DIR / f"{stem}.mp4")], check=True)
    Image.open(work / "f000.png").convert("RGB").save(OUT_DIR / f"{stem}.webp", quality=82)
    vtt = ["WEBVTT", ""] + [f"{vtt_time(c.start)} --> {vtt_time(c.end)} line:98%,end\n{c.text}\n" for c in cues]
    (OUT_DIR / f"{stem}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    print(f"chapter {chapter}: {t / 60:.1f} min, {len(scenes)} scenes", file=sys.stderr)
    return {"src": f"media/lectures/{stem}.mp4", "poster": f"media/lectures/{stem}.webp",
            "track": f"media/lectures/{stem}.vtt", "duration": round(t, 1), "outline": outline}


def write_manifest(entries: dict[int, dict]) -> None:
    existing: dict[str, dict] = {}
    if MANIFEST.exists():
        raw = MANIFEST.read_text(encoding="utf-8")
        existing = json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
    existing.update({str(k): v for k, v in entries.items()})
    ordered = dict(sorted(existing.items(), key=lambda kv: int(kv[0])))
    MANIFEST.write_text("export const lectures=" + json.dumps(ordered, ensure_ascii=False) + ";\n", encoding="utf-8")


async def main(chapters: list[int]) -> None:
    CACHE.mkdir(exist_ok=True)
    entries = {}
    for ch in chapters:
        entries[ch] = await build_chapter(ch)
        write_manifest(entries)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    requested = [int(a) for a in sys.argv[1:]] or sorted(int(p.stem[2:]) for p in SCRIPTS.glob("ch*.json"))
    asyncio.run(main(requested))
