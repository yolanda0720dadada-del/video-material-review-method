# Contributing

Contributions are welcome.

## Useful Improvements

- Better Set grouping heuristics
- More output formats, such as Notion, Feishu, Airtable, or Google Sheets
- Better scene description prompts for vision models
- More robust transcript confidence filtering
- Example configs for different content types

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the CLI:

```bash
vlog-material-review examples/project_config.example.json
```

## Privacy

Do not commit raw video, screenshots, generated outputs, transcripts, credentials, or private project configs.

The `.gitignore` is intentionally strict about common media and output folders.
