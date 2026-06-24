# AI-Assisted Workflow

The default CLI is intentionally local-first. It does not require cloud APIs.

For better results, use AI as a review layer after local extraction.

## Recommended Pipeline

1. Run the CLI to generate:
   - metadata
   - representative frames
   - rough Set grouping
   - optional rough transcript

2. Review representative frames with a vision model:
   - Identify scene
   - Identify action
   - Decide whether neighboring clips belong to the same Set
   - Flag clips that need more screenshots

3. Review transcript with project context:
   - Keep clear speech
   - Summarize noisy dialogue
   - Delete hallucinations
   - Leave uncertain speech blank

4. Export to your editing workflow:
   - Feishu / Lark document
   - Notion database
   - CSV for spreadsheet
   - HTML for local review

## Prompt Skeleton For Vision Review

```text
You are organizing video materials before rough cut editing.

Project context:
- Theme:
- Timeline:
- Important locations:
- Important people:
- Important keywords:

For each clip, inspect the representative frames and return:
1. Scene name
2. What happens in the clip
3. Whether it belongs to the same Set as neighboring clips
4. Whether it is replaceable with other clips
5. Whether more screenshots are needed
```

## Prompt Skeleton For Transcript Review

```text
You are cleaning rough ASR transcripts for a Vlog editing material table.

Rules:
1. Preserve clear speech.
2. Summarize noisy multi-person dialogue.
3. Use project context and frame content to fix obvious terms.
4. Do not invent details when audio is unclear.
5. Leave low-confidence or hallucinated content blank.

Project context:
- Theme:
- Timeline:
- Locations:
- Keywords:

Clip:
- filename:
- Set:
- rough transcript:
- frame description:
```
