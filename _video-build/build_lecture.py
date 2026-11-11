"""Render narrated Vietnamese lecture videos from chapter scripts.

Usage: python -I build_lecture.py 1 2 3   (no args = all chapters with a script)

Each scripts/chNN.json holds scenes; each scene has points, and each point is one
narration segment plus what it reveals on screen (a bullet, a table row, a code
line or a grid). The schema lives in script_model.py, the drawing in slides.py.
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

sys.path.insert(0, str(Path(__file__).resolve().parent))  # `python -I` leaves the script folder off sys.path

import edge_tts
import imageio_ffmpeg
from PIL import Image

from script_model import ROOT, SCRIPTS, SITE, check_assets, load_script
from slides import chapter_frames, draw, latex_to_unicode, slide_page

CACHE = ROOT / "cache"
OUT_DIR = SITE / "media" / "lectures"
MANIFEST = SITE / "lecture-data.js"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

VOICE = "vi-VN-HoaiMyNeural"
RATE = "-4%"
SAMPLE_RATE = 24000
POINT_GAP = 0.45  # seconds of silence after each point
SCENE_GAP = 0.9  # extra silence when a scene ends


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
    script = load_script(chapter)
    problems = check_assets(chapter, script)
    if problems:
        raise SystemExit("Script problems:\n" + "\n".join(problems))
    scenes = script.scenes
    work = CACHE / f"ch{chapter:02d}"
    work.mkdir(parents=True, exist_ok=True)
    for stale in work.glob("f*.png"):
        stale.unlink()

    frames = chapter_frames(chapter, script)
    speeches = await asyncio.gather(*[synthesize(p.say) for s in scenes for p in s.points])

    overflow: list[str] = []
    async with slide_page() as page:
        for n, frame in enumerate(frames):
            for problem in await draw(page, frame, work / f"f{n:03d}.png"):
                overflow.append(f"'{scenes[frame.scene_index].title}' point {frame.point_index + 1}: {problem}")
    if overflow:
        raise SystemExit(f"chapter {chapter}: text overflows its box\n" + "\n".join(sorted(set(overflow))))

    pcm = bytearray()
    t = 0.0
    concat_lines: list[str] = []
    cues: list[Cue] = []
    outline: list[dict] = []
    for n, (frame, sp) in enumerate(zip(frames, speeches)):
        scene = scenes[frame.scene_index]
        if frame.point_index == 0:
            outline.append({"title": latex_to_unicode(scene.title), "start": round(t, 2)})
        gap = POINT_GAP + (SCENE_GAP if frame.point_index == len(scene.points) - 1 else 0)
        with wave.open(str(sp.wav)) as w:
            pcm.extend(w.readframes(w.getnframes()))
        pcm.extend(silence(int(gap * SAMPLE_RATE)))
        cues.extend(piece for c in sp.cues for piece in split_cue(Cue(t + c.start, t + c.end, c.text)))
        seg = sp.duration + gap
        concat_lines += [f"file '{(work / f'f{n:03d}.png').as_posix()}'", f"duration {seg:.3f}"]
        t += seg
    concat_lines.append(f"file '{(work / f'f{len(frames) - 1:03d}.png').as_posix()}'")

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
    ends = [part["start"] for part in outline[1:]] + [t]
    chapters = ["WEBVTT", ""] + [f"{vtt_time(part['start'])} --> {vtt_time(end)}\n{part['title']}\n"
                                 for part, end in zip(outline, ends)]
    (OUT_DIR / f"{stem}.chapters.vtt").write_text("\n".join(chapters), encoding="utf-8")
    print(f"chapter {chapter}: {t / 60:.1f} min, {len(scenes)} scenes, {len(frames)} frames", file=sys.stderr)
    return {"src": f"media/lectures/{stem}.mp4", "poster": f"media/lectures/{stem}.webp",
            "track": f"media/lectures/{stem}.vtt", "chapters": f"media/lectures/{stem}.chapters.vtt",
            "duration": round(t, 1), "outline": outline}


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
