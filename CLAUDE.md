# CLAUDE.md

## Project Overview
This repository contains a small People Analytics case study for BrightPath Manufacturing.
The goal is to analyze employee attrition using Python and improve the codebase safely.

## What Good Work Looks Like
- Keep solutions simple and beginner-friendly
- Prefer readable pandas code over clever code
- Explain business meaning, not just code changes
- Preserve the column names in the raw CSV unless the task requires otherwise

## When Editing Code
- Change only what is needed for the task
- Avoid broad refactors unless asked
- Before major edits, briefly state the plan
- After edits, recommend how to verify the result

## Analysis Expectations
Focus on patterns tied to:
- department
- overtime
- travel frequency
- job satisfaction
- monthly income

## Testing
Run:
- `pytest`
- `python src/analyze_attrition.py`
