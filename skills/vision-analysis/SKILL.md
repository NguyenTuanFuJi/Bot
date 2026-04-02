---
name: vision-analysis
description: Analyze images, screenshots, diagrams, charts, mockups, and photos. Use when the user shares an image file or asks to describe, review, interpret, OCR, extract text from, or explain what is shown in an image. Also use for UI review, chart reading, object identification, and extracting visible details from visual input.
---

# Vision Analysis

Use this skill when a request depends on understanding an image.

## Common tasks
- Describe a photo or screenshot
- Extract visible text
- Review a UI or mockup
- Read a chart or diagram
- Identify objects, people, or activities
- Summarize what matters in an image for the user’s goal

## Workflow

1. Identify the image task
Choose the closest mode:
- describe
- OCR
- UI review
- chart analysis
- object / scene analysis

2. Focus on the user’s actual question
Do not describe everything if the user only wants:
- the text
- the issue in the design
- the data trend
- the main object or detail

3. Return structured results
Use a format that matches the task:
- description -> clear prose
- OCR -> text-first, preserve structure
- UI review -> strengths / issues / suggestions
- chart -> values / trend / takeaway
- object analysis -> itemized list

## Quality rules
- Distinguish what is clearly visible from what is uncertain
- Do not invent unreadable text
- Keep OCR faithful to the image
- For UI critique, give specific and actionable feedback
- For charts, separate visible data from inferred conclusions

## Suggested response patterns

### Description
- Main subject
- Setting / context
- Important visible details
- Why it matters to the user’s question

### OCR
- Extracted text
- Notes on unreadable or partial text if needed

### UI review
- Strengths
- Issues
- Suggested improvements

### Chart / diagram
- What is shown
- Key values or labels visible
- Main trend or conclusion

Use this skill only when visual understanding is central to the request.