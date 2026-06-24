# Tooling

This project is designed to be reusable without requiring private APIs.

## Video Understanding

Default video processing uses:

- `ffprobe` for metadata:
  - duration
  - creation time
  - stream information
- `ffmpeg` for representative screenshots:
  - 1 frame for short/simple clips
  - 2-3 frames for long clips or clips likely to change visually

The generated screenshots are meant for human or AI-assisted review. The default script does not force a specific cloud vision model.

Optional AI vision workflow:

1. Generate representative frames.
2. Send selected frames to your preferred vision model.
3. Ask it to infer scene, action, people, and replacement Set.
4. Keep human review in the loop for ambiguous material.

## Audio Understanding

Default transcription is optional.

When enabled, the script uses `faster-whisper` locally:

```bash
pip install faster-whisper
```

Recommended models:

| Model | Use Case |
|---|---|
| `small` | Fast rough transcript |
| `medium` | Better Mandarin recognition, slower |
| `large-v3-turbo` | Better quality when available, larger download |

Important: automatic transcripts should be treated as drafts.

For editing use, prefer:

- clear speech: preserve and punctuate
- noisy dialogue: summarize
- uncertain speech: leave blank
- hallucinated text: delete

## Output Files

The CLI generates:

- `rows.json`: structured source of truth
- `material_review.csv`: spreadsheet-friendly table
- `material_review.md`: Markdown table
- `material_review.html`: visual local preview with screenshots
- `frames/`: representative screenshots

## External Document Upload

This repo intentionally does not hardcode Feishu, Notion, Google Docs, or Airtable credentials.

Recommended flow:

1. Generate local review files.
2. Check the HTML preview.
3. Import CSV/Markdown into your document tool.
4. If you have an API integration, upload `rows.json` and frame files from there.
