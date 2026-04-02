---
name: minimax-docx
description: Create, edit, fill, or reformat Word documents in .docx format using the bundled OpenXML-based workflow. Use whenever the user wants a formal document such as a report, proposal, contract, memo, letter, filled form, or template-matched Word file. Also use when the user asks to modify or restyle an existing .docx without breaking formatting.
---

# MiniMax DOCX

Use this skill whenever the final deliverable is a `.docx` file or a formal Word-style document.

## Core routing

### A. Create
Use when there is no input `.docx` and the user wants a new document.
Read first:
- `references/scenario_a_create.md`

### B. Edit / Fill
Use when there is an existing `.docx` and the user wants to:
- replace text
- fill placeholders
- update sections
- add or remove content
Read first:
- `references/scenario_b_edit_content.md`

### C. Apply template / reformat
Use when there is an input `.docx` and a formatting target or template.
Read first:
- `references/scenario_c_apply_template.md`

## Required operating flow

1. Check environment
- first setup if needed: `bash scripts/setup.sh`
- first session check: `bash scripts/env_check.sh`

2. Preview and inspect before editing existing files
- `bash scripts/docx_preview.sh document.docx`
- use the bundled analyze flow when the task requires structure awareness

3. Choose the correct execution path
- simple content operations -> use CLI
- structural document manipulation -> use the bundled OpenXML C# path

4. Validate after every write
Minimum checks:
- merge runs if needed
- validate structure
- validate business rules
- preview final output

## Key rules
- Always use this skill for `.docx` work instead of ad-hoc text generation alone
- Preserve formatting integrity on edit tasks
- For complex structural edits, prefer the OpenXML code path over fragile shortcuts
- For template application, do not deliver until validation passes
- If the task involves CJK or official formatting, read the matching reference before editing

## Read references as needed
### Core scenarios
- `references/scenario_a_create.md`
- `references/scenario_b_edit_content.md`
- `references/scenario_c_apply_template.md`

### Typography and design
- `references/typography_guide.md`
- `references/design_principles.md`
- `references/cjk_typography.md`
- `references/cjk_university_template_guide.md`

### OpenXML safety
- `references/openxml_element_order.md`
- `references/openxml_units.md`
- `references/troubleshooting.md`
- `references/xsd_validation_guide.md`

## Bundled tools
- `scripts/docx_preview.sh`
- `scripts/doc_to_docx.sh`
- `scripts/env_check.sh`
- `scripts/setup.sh`
- `scripts/dotnet/`

Use the references folder for the detailed patterns. Keep SKILL.md focused on routing and safe execution.