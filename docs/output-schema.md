# Output Schema

The CLI writes `rows.json` as the structured source of truth.

## Row

```json
{
  "filename": "IMG_0001.MOV",
  "path": "/absolute/path/to/IMG_0001.MOV",
  "created": "2026-04-02 13:42:14",
  "duration": "22.9 秒",
  "set": "Set 001：待命名场景",
  "speech": "",
  "frames": [
    "frames/001_IMG_0001_rep1.jpg"
  ]
}
```

## Fields

| Field | Meaning |
|---|---|
| `filename` | Original source filename |
| `path` | Absolute source path |
| `created` | Shooting / file creation time |
| `duration` | Human-readable duration |
| `set` | Scene grouping label |
| `speech` | Cleaned or rough speech text |
| `frames` | Relative paths to representative screenshots |

## Generated Outputs

| File | Purpose |
|---|---|
| `rows.json` | Structured data for integrations |
| `material_review.csv` | Spreadsheet import |
| `material_review.md` | Markdown document |
| `material_review.html` | Visual local preview |
| `frames/` | Representative screenshots |
