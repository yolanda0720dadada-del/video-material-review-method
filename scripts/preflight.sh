#!/usr/bin/env bash
set -u

ok=1

echo "▶ Checking prerequisites for vlog-material-review..."
echo

if command -v python3 >/dev/null 2>&1; then
  py_version="$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')"
  echo " ✓ Python ${py_version}"
else
  echo " ✗ python3 not found"
  ok=0
fi

if command -v ffmpeg >/dev/null 2>&1; then
  echo " ✓ ffmpeg ($(ffmpeg -version 2>/dev/null | head -1))"
else
  echo " ✗ ffmpeg not found"
  echo "   Install on macOS: brew install ffmpeg"
  ok=0
fi

if command -v ffprobe >/dev/null 2>&1; then
  echo " ✓ ffprobe available"
else
  echo " ✗ ffprobe not found"
  echo "   It is usually installed with ffmpeg."
  ok=0
fi

python3 - <<'PY'
try:
    import faster_whisper  # noqa: F401
except Exception:
    print(" ! faster-whisper not installed; transcription is optional")
else:
    print(" ✓ faster-whisper available")
PY

echo
if [ "$ok" = 1 ]; then
  echo "✅ Ready for local video material review."
else
  echo "❌ Missing required prerequisites above."
  exit 1
fi
