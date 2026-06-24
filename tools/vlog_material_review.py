#!/usr/bin/env python3
import csv
import html
import json
import math
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


VIDEO_EXTENSIONS = {".mov", ".mp4", ".m4v", ".avi", ".mkv"}


@dataclass
class ClipInfo:
    index: int
    filename: str
    path: Path
    created: str
    duration_seconds: float
    set_name: str
    speech: str
    frames: list[str]


def require_binary(name: str) -> str:
    found = shutil.which(name)
    if not found:
        raise SystemExit(f"Missing required binary: {name}. Please install ffmpeg first.")
    return found


def run_json(cmd: list[str]) -> dict:
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return json.loads(result.stdout)


def parse_creation_time(metadata: dict, fallback_path: Path) -> datetime:
    tags = (metadata.get("format") or {}).get("tags") or {}
    value = tags.get("creation_time") or tags.get("com.apple.quicktime.creationdate")
    if value:
        value = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(value).replace(tzinfo=None)
        except ValueError:
            pass
    return datetime.fromtimestamp(fallback_path.stat().st_mtime)


def probe_clip(path: Path) -> tuple[datetime, float]:
    metadata = run_json([
        "ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ])
    created = parse_creation_time(metadata, path)
    duration = float((metadata.get("format") or {}).get("duration") or 0)
    return created, duration


def duration_label(seconds: float) -> str:
    if seconds >= 60:
        minutes = int(seconds // 60)
        rest = round(seconds % 60)
        return f"{minutes}分{rest:02d}秒"
    return f"{seconds:.1f} 秒"


def pick_frame_times(duration: float, default_frames: int, long_threshold: float, long_frames: int) -> list[float]:
    count = long_frames if duration >= long_threshold else default_frames
    count = max(1, count)
    if count == 1:
        return [max(0.2, duration * 0.35)]
    return [duration * p for p in (0.18, 0.5, 0.82)[:count]]


def extract_frames(path: Path, out_dir: Path, index: int, config: dict) -> list[str]:
    policy = config.get("frame_policy") or {}
    default_frames = int(policy.get("default_frames", 1))
    long_threshold = float(policy.get("long_video_threshold_seconds", 30))
    long_frames = int(policy.get("long_video_frames", 3))
    _, duration = probe_clip(path)
    times = pick_frame_times(duration, default_frames, long_threshold, long_frames)

    out_dir.mkdir(parents=True, exist_ok=True)
    rels = []
    stem = safe_stem(path.stem)
    for frame_index, timestamp in enumerate(times, 1):
        frame_name = f"{index:03d}_{stem}_rep{frame_index}.jpg"
        frame_path = out_dir / frame_name
        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            str(path),
            "-frames:v",
            "1",
            "-q:v",
            "3",
            str(frame_path),
        ]
        subprocess.run(cmd, check=True)
        rels.append(f"frames/{frame_name}")
    return rels


def safe_stem(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in value)


def transcribe_clip(path: Path, config: dict) -> str:
    trans_cfg = config.get("transcription") or {}
    if not trans_cfg.get("enabled"):
        return ""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise SystemExit("Transcription is enabled but faster-whisper is not installed.")

    model_name = trans_cfg.get("model", "small")
    language = trans_cfg.get("language", "zh")
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(
        str(path),
        language=language,
        vad_filter=True,
        beam_size=5,
        best_of=5,
        temperature=0,
        condition_on_previous_text=False,
    )
    parts = [seg.text.strip() for seg in segments if seg.text.strip()]
    return normalize_speech("".join(parts))


def normalize_speech(text: str) -> str:
    text = " ".join((text or "").split())
    if len(text) <= 1:
        return ""
    return text


def infer_sets(clips: list[tuple[Path, datetime, float]]) -> list[str]:
    sets = []
    current = 1
    previous_time = None
    for _, created, _ in clips:
        if previous_time is not None:
            gap = (created - previous_time).total_seconds()
            if gap > 180:
                current += 1
        sets.append(f"Set {current:03d}：待命名场景")
        previous_time = created
    return sets


def scan_videos(input_dir: Path) -> list[Path]:
    return sorted(
        [p for p in input_dir.rglob("*") if p.suffix.lower() in VIDEO_EXTENSIONS],
        key=lambda p: p.name,
    )


def build_rows(config: dict) -> list[ClipInfo]:
    require_binary("ffmpeg")
    require_binary("ffprobe")

    input_dir = Path(config["input_dir"]).expanduser()
    output_dir = Path(config.get("output_dir", "outputs/material_review")).expanduser()
    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir
    frame_dir = output_dir / "frames"
    output_dir.mkdir(parents=True, exist_ok=True)

    videos = scan_videos(input_dir)
    probed = []
    for path in videos:
        created, duration = probe_clip(path)
        probed.append((path, created, duration))
    probed.sort(key=lambda item: (item[1], item[0].name))
    set_names = infer_sets(probed)

    rows = []
    for index, ((path, created, duration), set_name) in enumerate(zip(probed, set_names), 1):
        frames = extract_frames(path, frame_dir, index, config)
        speech = transcribe_clip(path, config)
        rows.append(ClipInfo(
            index=index,
            filename=path.name,
            path=path,
            created=created.strftime("%Y-%m-%d %H:%M:%S"),
            duration_seconds=duration,
            set_name=set_name,
            speech=speech,
            frames=frames,
        ))
        print(f"{index:03d}/{len(probed)} {path.name}")
    return rows


def row_dict(row: ClipInfo) -> dict:
    return {
        "filename": row.filename,
        "path": str(row.path),
        "created": row.created,
        "duration": duration_label(row.duration_seconds),
        "set": row.set_name,
        "speech": row.speech,
        "frames": row.frames,
    }


def write_outputs(rows: list[ClipInfo], config: dict) -> None:
    output_dir = Path(config.get("output_dir", "outputs/material_review")).expanduser()
    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir
    data = [row_dict(r) for r in rows]

    (output_dir / "rows.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(output_dir / "material_review.csv", data)
    write_markdown(output_dir / "material_review.md", data, config)
    write_html(output_dir / "material_review.html", data, config)


def write_csv(path: Path, data: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "created", "duration", "set", "speech", "frames"])
        writer.writeheader()
        for row in data:
            item = dict(row)
            item["frames"] = "; ".join(row["frames"])
            writer.writerow(item)


def write_markdown(path: Path, data: list[dict], config: dict) -> None:
    lines = [f"# {config.get('project_name', 'Material Review')}", ""]
    lines.append("| 候选素材名称 | 拍摄时间 | 视频时长 | 大场景 / Set | 口播内容 | 代表截图 |")
    lines.append("|---|---|---:|---|---|---|")
    for row in data:
        frames = "<br>".join(row["frames"])
        lines.append(
            f"| {escape_md(row['filename'])} | {row['created']} | {row['duration']} | "
            f"{escape_md(row['set'])} | {escape_md(row['speech'])} | {escape_md(frames)} |"
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def escape_md(value: str) -> str:
    return (value or "").replace("|", "\\|").replace("\n", "<br>")


def write_html(path: Path, data: list[dict], config: dict) -> None:
    title = html.escape(config.get("project_name", "Material Review"))
    rows = []
    for row in data:
        imgs = "".join(
            f'<figure><img src="{html.escape(frame)}" alt=""><figcaption>{html.escape(Path(frame).name)}</figcaption></figure>'
            for frame in row["frames"]
        )
        rows.append(
            "<tr>"
            f"<td>{html.escape(row['filename'])}</td>"
            f"<td>{html.escape(row['created'])}</td>"
            f"<td>{html.escape(row['duration'])}</td>"
            f"<td>{html.escape(row['set'])}</td>"
            f"<td>{html.escape(row['speech'])}</td>"
            f"<td class='frames'>{imgs}</td>"
            "</tr>"
        )

    doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 24px; color: #1f2328; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #d0d7de; padding: 10px; vertical-align: top; }}
    th {{ background: #f6f8fa; text-align: left; }}
    td.frames {{ min-width: 220px; }}
    figure {{ margin: 0 0 10px; }}
    img {{ max-width: 220px; height: auto; display: block; }}
    figcaption {{ color: #6e7781; font-size: 12px; margin-top: 4px; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <table>
    <thead>
      <tr><th>候选素材名称</th><th>拍摄时间</th><th>视频时长</th><th>大场景 / Set</th><th>口播内容</th><th>代表截图</th></tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</body>
</html>"""
    path.write_text(doc, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/vlog_material_review.py path/to/project_config.json")
    config = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    rows = build_rows(config)
    write_outputs(rows, config)
    print(f"Done. Output: {config.get('output_dir', 'outputs/material_review')}")


if __name__ == "__main__":
    main()
