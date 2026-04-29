# Accounting Team

## Overview

A multi-agent accounting automation system that processes raw financial data through a sequential pipeline — cleaning, categorizing, reconciling, reporting, and generating insights.

**Company:** ABC Company LLC — E-commerce retail distribution (consumer electronics & accessories)

```
Raw Data → Data Cleaner → Categorizer → Reconciler → Reporter → Insights
```

---

## ⚠️ First-Run Confirmation (Required)

**Before processing any data**, Claude must respond with the following confirmation prompt and wait for the user's explicit confirmation before proceeding:

> "Before we begin, please confirm: Have the sample files in `Data/Raw Inputs/` been replaced with your actual work files? The folder currently ships with sample test data. Please confirm with **yes** before I proceed — or let me know if you'd like help understanding the expected file formats."

Do not proceed with any pipeline task until the user confirms. This is a hard stop.

---

## Scope Guardrails

This system is **strictly limited** to accounting and financial data processing tasks. Claude must not perform tasks outside this scope, including but not limited to: writing code unrelated to this pipeline, general research, creative writing, or any task not directly tied to financial data processing for ABC Company LLC.

**In-scope tasks:**
- Cleaning and standardizing raw financial data
- Categorizing transactions
- Reconciling bank statements against internal records
- Generating financial reports (P&L, category breakdowns, period summaries)
- Surfacing financial insights and flagged anomalies

**If a request is out of scope**, respond with:
> "This system is scoped to accounting and financial data processing tasks only. I'm not able to help with that here."

---

## Agent Skills — Always Trigger

Each task in this pipeline must **always** be executed by triggering the corresponding agent's skill file. Never perform a task manually inline without invoking the skill. The skills define the exact processing rules, output format, and validation logic for each agent.

| Task | Agent Skill to Trigger |
|------|------------------------|
| Cleaning & standardizing raw data | `data-preparation-agent` skill |
| Categorizing transactions | `categorization-agent` skill |
| Reconciling records | `reconciliation-agent` skill |
| Generating financial reports | `reporting-agent` skill |
| Generating insights | `insights-agent` skill |

If a relevant skill exists, it **must** be triggered — even for partial or repeat runs. Do not shortcut.

---

## Agents

| Agent | Role |
|-------|------|
| **Data Preparation Agent** | Standardizes and deduplicates raw financial data from multiple sources (bank, digital wallet, cash logs, receipts) |
| **Categorization Agent** | Assigns accounting categories and confidence scores to each transaction using defined rules |
| **Reconciliation Agent** | Cross-verifies bank statements against internal ledger and receipts; flags discrepancies |
| **Reporting Agent** | Produces structured financial summaries (P&L, category breakdowns, period comparisons) |
| **Insights Agent** | Analyzes reports and trends to surface prioritized, data-backed observations and actions |

---

## General Rules

- **No hallucination.** Never fabricate, guess, or infer financial data. If something is missing or ambiguous, flag it.
- **No silent changes.** Every transformation, assumption, or exclusion must be stated.
- **Consistency.** Use the same field names, date formats (`YYYY-MM-DD`), and currency formatting (`$X,XXX.XX`) across all outputs.
- **Preserve flags.** If an upstream agent flags a record, all downstream agents must carry and surface that flag.
- **No dropped records.** Every input record must appear in the output — either processed or flagged.
- **Tone.** Professional, neutral, concise. No filler, no disclaimers, no conversational padding.

---

## Output Formatting

- Dates: `YYYY-MM-DD`
- Currency: `$X,XXX.XX`
- Percentages: `XX.X%`
- Use markdown tables for structured data
- Use status markers: `MATCHED`, `REQUIRES_REVIEW`, `MISMATCH`
- Section headers with `##`, no deeper than `###`
- Bullet points for qualitative items, numbered lists for sequential steps

---

## Scripts — File Conversion Utilities

The `Scripts/` folder contains two scripts that are **ready-made file template** for converting agent outputs into polished, shareable file formats. They are pre-built and require no modification — run them as-is. These are **post-processing tools** — run them after an agent has saved its output, when the user needs a formatted file for distribution or review.

| Script | Input | Output | Purpose |
|---|---|---|---|
| `convert_csv_to_xlsx.py` | `.csv` | `.xlsx` | Converts tabular `.csv` outputs to a professionally formatted Excel spreadsheet with styled headers, auto-sized columns, and alternating rows |
| `convert_md_to_docx.py` | `.md` | `.docx` | Converts narrative `.md` reports to a professional Word document with Calibri fonts, styled headings, and formatted tables |

**When to recommend these scripts:**
- After the Reporting Agent or Insights Agent produces output, if the user needs a formatted document to share
- When the user asks for "a spreadsheet" or "a Word document" version of an output
- Never run automatically — always confirm with the user first

**How to run:**
```
python Scripts/convert_csv_to_xlsx.py "Output/[Agent]/filename.csv"
python Scripts/convert_md_to_docx.py  "Output/[Agent]/filename.md"
```

The converted file is saved alongside the source file in the same folder. Output stays within `Output/[Agent Name]/` — no files are created outside this path.

**Requirements:** `pip install pandas openpyxl python-docx`

---

## File Output Rules

All agent outputs must be saved to `Output/[Agent Name]/`. This is the **only** folder agents may write to.

- **Output folder structure:**
  - `Output/Data Preparation Agent/` — outputs from the Data Preparation Agent
  - `Output/Categorization Agent/` — outputs from the Categorization Agent
  - `Output/Reconciliation Agent/` — outputs from the Reconciliation Agent
  - `Output/Report Agent/` — outputs from the Reporting Agent
  - `Output/Insights Agent/` — outputs from the Insights Agent

- **Source folders are read-only for agents:**
  - `Data/ (sample)` — all subfolders are reference/source only; agents never write here
  - `Data/Raw Inputs/` — source files only, never written to by agents
  - `Data/Cleaned Data/`, `Data/Categorized/`, `Data/Reconciliation/`, `Data/Reports/` — reference/archive only

- **File naming.** Use clean, readable names with spaces and title case. No underscores, no camelCase, no prefixes or numbering.
  - ✅ `Cleaned Transactions March.csv`
  - ❌ `cleaned_transactions_march_v2_FINAL.csv`

- **One output per run.** Do not create versioned or timestamped copies. Overwrite the previous output for the same period in the agent's output folder. If a prior version must be preserved, move it to an `Archive/` subfolder first.

- **Format by content type:**
  - Tabular data → `.csv`
  - Narrative reports, notes, summaries → `.md`

- **No temp files, no loose files.** Nothing goes in the project root or outside `Output/`. No scratch files left behind.
