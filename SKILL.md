---
name: vlog-material-review
version: 0.1.0
description: >
  A reusable workflow and CLI for organizing Vlog / travel / daily-life video materials before rough cut editing.
  Use this when the user has many raw video clips and wants a searchable material review table with shooting time,
  duration, scene Set grouping, usable speech notes, and representative screenshots.
---

# Vlog Material Review

This skill helps an agent turn a folder of raw Vlog clips into a practical rough-cut material table.

It is not a full automatic editor. The CLI creates the local source of truth; the agent reviews frames and transcripts, corrects Set grouping and speech notes, then exports to a document or editing workflow.

## When To Use

- The user has many raw clips and wants them organized before editing.
- The user wants to identify repeated scenes and interchangeable candidate clips.
- The user wants representative screenshots for fast visual scanning.
- The user wants rough or cleaned speech notes for subtitles, narration, or clip selection.
- The user wants a local HTML / CSV / Markdown preview, or a document-friendly output.

## Step 0: Prerequisites

Run:

```bash
bash scripts/preflight.sh
```

Required:

- Python 3.10+
- `ffmpeg`
- `ffprobe`

Optional:

- `faster-whisper` for local speech recognition

If prerequisites are missing, tell the user what to install and stop before processing.

## Conversation Flow

1. Understand the project:
   - video theme
   - raw material folder
   - timeline or itinerary
   - important locations, names, brands, and keywords
   - target editing tool

2. Create or update a project config from `examples/project_config.example.json`.

3. Run the CLI:

```bash
vlog-material-review my_project.json
```

or:

```bash
python tools/vlog_material_review.py my_project.json
```

4. Review the generated `material_review.html`:
   - check representative screenshots
   - adjust Set names
   - decide whether clips are interchangeable
   - clean transcript notes

5. Deliver:
   - local preview path
   - structured `rows.json`
   - CSV / Markdown table
   - any online document link if an integration is used

## Files

- `RULES.md`: hard rules for material review quality.
- `CATALOG.md`: output modes and review modes.
- `docs/tooling.md`: exact toolchain.
- `docs/ai-workflow.md`: optional AI-assisted frame and transcript review.
- `docs/output-schema.md`: `rows.json` schema.
- `tools/vlog_material_review.py`: local CLI.
- `scripts/preflight.sh`: dependency check.
