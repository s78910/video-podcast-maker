# Design Learning

Extract visual design patterns from reference videos or images, store them in a searchable library, and apply them to new video compositions.

> **When to load:** Only when the user runs `/design-learn`, provides a reference video/image, or asks to save/list/delete style profiles. Skip for normal video creation flow.

---

## Commands

```bash
# Learn from images (use your agent's image analysis capability to analyze design patterns)
python3 scripts/learn_design.py ./screenshot1.png ./screenshot2.png

# Learn from a local video (ffmpeg extracts frames automatically)
python3 scripts/learn_design.py ./reference.mp4

# Learn from a URL (Playwright captures screenshots — experimental)
python3 scripts/learn_design.py https://www.bilibili.com/video/BV1xx411c7mD

# Save with a named profile and tags
python3 scripts/learn_design.py ./reference.mp4 --profile "tech-minimal" --tags "tech,minimal,dark"
```

## Reference Library Commands

```
references list          # List all stored references (auto-cleans orphaned entries)
references show <id>     # Show full design report for a reference
references delete <id>   # Delete a reference and its files
```

## Style Profile Commands

```
profiles list            # List all saved style profiles
profiles show <name>     # Show profile props_override
profiles delete <name>   # Delete a style profile
profiles create <name>   # Create a new style profile interactively
```

---

## Pre-Workflow Usage

When the user provides a reference video or image alongside a video creation request, extract design patterns **before Step 1** and apply them as session overrides.

See `references/workflow-script.md` → Pre-workflow section for the full extraction flow.

## Step 9 Integration

Before choosing visual design in Step 9, check for matching style profiles or reference library entries. Apply the best match as a starting point for Remotion composition props.

See `references/workflow-production.md` → Step 9 Style Profile Integration for the priority chain.

---

## Troubleshooting

Common issues (ffmpeg not found, Playwright fails, orphaned references, style profile not applied) are covered in **`references/troubleshooting.md`** → "Design Learning Troubleshooting" section.
