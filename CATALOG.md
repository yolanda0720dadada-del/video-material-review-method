# Review Mode Catalogue

Use this catalogue to choose a workflow mode.

## Modes

| Mode | Best For | Output Style |
|---|---|---|
| `quick-scan` | Fast first pass through many clips | Sparse speech, 1 screenshot, rough Set |
| `rough-cut` | Preparing actual editing decisions | Clean Set grouping, usable speech notes, representative screenshots |
| `speech-focused` | Vlogs where narration matters | More careful ASR and transcript cleanup |
| `visual-first` | Montage, travel scenery, B-roll | More screenshots, lighter speech |
| `handoff` | Giving material to another editor | Cleaner names, conservative notes, fewer uncertain claims |

## Choosing A Mode

- Use `quick-scan` when the user only wants to see what is in the folder.
- Use `rough-cut` by default.
- Use `speech-focused` when oral narration drives the video.
- Use `visual-first` when the footage is mostly scenery, food, objects, or atmosphere.
- Use `handoff` when another person will edit from the table.

## Recommended Config Defaults

### quick-scan

```json
{
  "frame_policy": {
    "default_frames": 1,
    "long_video_threshold_seconds": 45,
    "long_video_frames": 2
  },
  "transcription": {
    "enabled": false
  }
}
```

### rough-cut

```json
{
  "frame_policy": {
    "default_frames": 1,
    "long_video_threshold_seconds": 30,
    "long_video_frames": 3
  },
  "transcription": {
    "enabled": false
  }
}
```

### speech-focused

```json
{
  "frame_policy": {
    "default_frames": 1,
    "long_video_threshold_seconds": 30,
    "long_video_frames": 2
  },
  "transcription": {
    "enabled": true,
    "model": "large-v3-turbo",
    "language": "zh",
    "keep_low_confidence": false
  }
}
```
