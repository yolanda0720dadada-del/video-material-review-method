# Material Review Rules

These rules apply to every project.

## Core Rules

- The table is for rough cut decisions, not for exhaustive description.
- Every row must keep the original filename as the material key.
- Sort clips by shooting time whenever possible.
- Group interchangeable clips into the same `Set`.
- Keep Set names short and practical.
- Use screenshots to help the editor recognize clips quickly.
- Do not force a speech note when the audio is unclear.

## Set Grouping

Same Set usually means:

- same location
- same action
- same topic
- repeated take of the same speech
- same visual subject from different angles

If two clips are visually similar and only one is likely to be used, put them in the same Set.

If a clip changes scene significantly, either:

- extract more screenshots, or
- split the interpretation manually during review.

## Screenshot Rules

- Short stable clip: 1 representative frame.
- Long moving shot: 2-3 representative frames.
- Same person, same angle, repeated speech: 1 frame is enough.
- Keep original aspect ratio.
- Do not crop to force a horizontal preview unless the user asks.

## Speech Rules

Speech notes are editing aids, not legal transcripts.

Use this hierarchy:

1. Clear close speech: keep the speech and add punctuation.
2. Noisy dialogue: summarize.
3. Unclear far speech, music, wind, or background broadcast: leave blank.
4. ASR hallucination or repeated nonsense: delete.

When correcting speech, use:

- project context
- Set name
- representative frames
- known locations, people, brands, and keywords

Do not invent details just because they fit the trip.

## AI Review Rules

- Treat ASR as a draft.
- Treat frame analysis as a draft.
- Human or agent review should prefer conservative blanks over confident nonsense.
- Low-confidence text should not pollute the material table.

## Output Rules

The generated table should be easy to scan:

- no oversized prose columns by default
- no duplicated content fields
- no private raw media paths in public examples
- no accidental upload of raw video files

The default fields are:

- material filename
- shooting time
- duration
- Set
- speech note
- representative screenshots
