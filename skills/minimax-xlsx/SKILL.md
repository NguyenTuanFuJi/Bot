---
name: minimax-xlsx
description: Create, read, analyze, edit, fix, or validate spreadsheet files such as .xlsx, .xlsm, .csv, and .tsv. Use when the user asks for spreadsheet creation, Excel editing, formula work, tabular analysis, formatting, validation, or zero-format-loss updates to an existing workbook.
---

# MiniMax XLSX

Use this skill for spreadsheet work where the result must stay in Excel-compatible form.

## Task routing

### READ
Use for analysis and extraction from an existing file.
Read first:
- `references/read-analyze.md`

### CREATE
Use when building a new spreadsheet from scratch.
Read first:
- `references/create.md`
- `references/format.md`

### EDIT
Use when modifying an existing workbook without losing formatting.
Read first:
- `references/edit.md`
- `references/format.md` if styling is involved

### FIX
Use when repairing formulas or workbook logic.
Read first:
- `references/fix.md`

### VALIDATE
Use when checking formulas or workbook integrity.
Read first:
- `references/validate.md`

## Required rules
- Always produce the output file the user asked for
- For existing workbooks, preserve sheets, data, and formatting unless the task explicitly changes them
- For Vietnamese spreadsheets, default text font must be **Times New Roman** unless the user explicitly requests another font
- Never use a lossy edit path for existing Excel files
- Use formula-based outputs for calculated cells instead of hardcoded values
- Validate before delivery when formulas or structural edits are involved

## Preferred execution model
- READ -> `xlsx_reader.py` and analysis tools
- CREATE -> template + XML-based generation
- EDIT / FIX -> unpack -> change -> repack
- VALIDATE -> formula checking and recalculation tools when available

## Core helper scripts
- `scripts/xlsx_reader.py`
- `scripts/xlsx_unpack.py`
- `scripts/xlsx_pack.py`
- `scripts/formula_check.py`
- `scripts/xlsx_add_column.py`
- `scripts/xlsx_insert_row.py`
- `scripts/xlsx_shift_rows.py`
- `scripts/libreoffice_recalc.py`

## Important editing rules
- Existing workbook edits must preserve the original workbook structure
- Only change the cells, rows, columns, or formulas requested
- Re-open or re-check the output after editing to confirm integrity
- When adding formulas, keep them as Excel formulas rather than replacing with static results

## Read references as needed
- `references/read-analyze.md`
- `references/create.md`
- `references/edit.md`
- `references/fix.md`
- `references/validate.md`
- `references/format.md`
- `references/ooxml-cheatsheet.md`

## Templates
- `templates/minimal_xlsx/`

Use SKILL.md for routing and safety rules. Use the references for exact implementation details.
