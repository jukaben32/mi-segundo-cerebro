---
name: reconciliation-agent
description: >
  Compares a cleaned bank statement against an internal ledger to identify
  matched transactions, mismatches, missing entries, and duplicates. Use when
  the user provides bank statement and ledger files and asks to reconcile,
  cross-check, or verify accounts. Trigger phrases: "reconcile transactions",
  "compare bank to ledger", "find discrepancies", "match bank statement",
  "what's unmatched", "run reconciliation", "check for mismatches". Accepts
  CSV files as primary input and optional reconciliation notes as context.
  Does NOT categorize, clean, or modify source files.
---

# Reconciliation Agent

Cross-verifies `Bank Statement March Clean.csv` against `Internal Ledger March.csv` using `Reconciliation Notes.md` as supporting context. Produces a structured reconciliation report identifying matched records, mismatches, missing entries, and duplicates.

## When to Use This Skill

- User provides a bank statement CSV and an internal ledger CSV
- User asks to reconcile, cross-check, or verify accounts for a period
- User wants to identify discrepancies before closing the books
- Output is being prepared for the Reporting or Insights Agent

## Source Files

| File | Location | Role |
|---|---|---|
| `Bank Statement March Clean.csv` | `Data/Cleaned Data/` | External source of truth — bank-recorded transactions |
| `Internal Ledger March.csv` | `Data/Reconciliation/` | Internal accounting records |
| `Reconciliation Notes.md` | `Data/Reconciliation/` | Prior notes, known issues, and resolved items — load as context |

All source files are **read-only**. Do not modify them.

## Input Schemas

### Bank Statement fields

| Field | Type | Notes |
|---|---|---|
| `date` | `YYYY-MM-DD` | Bank posting date |
| `description` | string | Bank-provided merchant or transaction description |
| `debit` | numeric or blank | Amount leaving the account |
| `credit` | numeric or blank | Amount entering the account |
| `balance` | numeric | Running balance after transaction |
| `status` | string | Pre-flagged status from cleaning stage (`clean`, `review_amount_mismatch`, `review_unidentified`) |

### Internal Ledger fields

| Field | Type | Notes |
|---|---|---|
| `entry_id` | string | Unique ledger entry identifier (e.g., `LED-0301-001`) |
| `date` | `YYYY-MM-DD` | Date transaction was recorded |
| `description` | string | Internal description of the transaction |
| `debit` | numeric or blank | Amount debited in ledger |
| `credit` | numeric or blank | Amount credited in ledger |
| `account` | string | Chart of accounts classification |
| `reference` | string or blank | Vendor invoice number, order ID, or tracking reference |
| `recorded_by` | string | Person or system that created the entry |

## Step 1: Load and Inspect Both Files

Before matching, report:

- Bank statement: total records, date range, total debits, total credits
- Internal ledger: total records, date range, total debits, total credits
- Any pre-flagged bank records (`status` ≠ `clean`) — list them upfront
- Load `Reconciliation Notes.md` as background context for known issues; do not treat its conclusions as final — re-derive results independently

State these findings before proceeding to matching.

## Step 2: Match Records

Match each bank record to a ledger entry using the following priority order:

### Matching rules (apply in order)

1. **Reference match (highest confidence):** Bank description contains a reference code that appears in the ledger `reference` field (e.g., `AZ-90347`, `INV-TS-4521`, `TRK-789456123`). Require same date and same amount to confirm.

2. **Exact match:** Same date + same amount (debit/credit direction consistent) + description similarity above ~70% (same merchant name or recognizable abbreviation).

3. **Date-tolerance match:** Same amount + description similarity, date within ±1 calendar day. Flag as `⚠️ REQUIRES_REVIEW` with note: `Date offset of N day(s) — confirm posting vs. recording date`.

4. **Amount-tolerance match:** Same date + description similarity, amount differs by any value. Classify as `❌ MISMATCH` — record both amounts and compute variance.

### Direction consistency

Before matching amounts, normalize direction:

- Bank `debit` matches ledger `debit` (money out)
- Bank `credit` matches ledger `credit` (money in)
- A bank debit matched to a ledger credit (or vice versa) is always a `❌ MISMATCH` regardless of amount

### Duplicate detection

Within each file independently:

- Flag any two records with identical `date` + `amount` + `description` (after trimming whitespace) as a potential duplicate
- Keep both — do not drop either
- Tag both with `⚠️ REQUIRES_REVIEW` and note: `Possible duplicate — verify with source`

## Step 3: Classify Every Record

After matching, assign each bank record and each ledger entry exactly one status:

| Status | Meaning |
|---|---|
| `✅ MATCHED` | Confirmed match across date, amount, and description |
| `❌ MISMATCH` | Match found but amounts differ — record variance |
| `⚠️ REQUIRES_REVIEW` | Date-offset match, pre-flagged status, or other uncertainty |
| `⚠️ BANK ONLY` | Bank record has no corresponding ledger entry |
| `⚠️ LEDGER ONLY` | Ledger entry has no corresponding bank record |

Every record from both files must receive a status. No record may be left unclassified.

## Step 4: Compute Reconciliation Totals

Calculate the following from the bank statement:

- **Bank opening balance:** balance of first record + debit of first record − credit of first record
- **Bank closing balance:** balance of last record
- **Total bank debits:** sum of all debit values
- **Total bank credits:** sum of all credit values

Calculate the following from the internal ledger:

- **Total ledger debits:** sum of all debit values
- **Total ledger credits:** sum of all credit values
- **Implied ledger net change:** total credits − total debits

Compute:

- **Unreconciled difference:** bank closing balance − (bank opening balance + ledger net change)
- List each unresolved discrepancy (MISMATCH, BANK ONLY, LEDGER ONLY) with its contribution to the difference

## Step 5: Produce the Reconciliation Report

Output a complete reconciliation report as a `.md` file saved to `Data/Output/Reconciliation Report March.md`.

### Report structure

```
## Reconciliation Report — March 2026
**Company:** ABC Company LLC
**Period:** 2026-03-01 to 2026-03-31
**Bank Source:** Bank Statement March Clean.csv
**Ledger Source:** Internal Ledger March.csv
**Prepared by:** Reconciliation Agent
**Date:** [today's date]

---

## Summary

| Metric | Count / Amount |
|---|---|
| Total bank transactions | N |
| Total ledger entries | N |
| ✅ Matched | N |
| ❌ Mismatch | N |
| ⚠️ Bank Only (missing from ledger) | N |
| ⚠️ Ledger Only (missing from bank) | N |
| ⚠️ Requires Review | N |
| Bank closing balance | $X,XXX.XX |
| Ledger net change | $X,XXX.XX |
| Unreconciled difference | $X,XXX.XX |

**Reconciliation Status:** COMPLETE | PARTIAL — [N] items require resolution

---

## ❌ Mismatches

For each mismatch, provide a structured entry:

### MISMATCH-[N]: [Short Description]

| Field | Bank | Ledger |
|---|---|---|
| Date | YYYY-MM-DD | YYYY-MM-DD |
| Description | [bank text] | [ledger text] |
| Amount | $X,XXX.XX | $X,XXX.XX |
| Reference | [if available] | [if available] |

- **Variance:** $X.XX ([bank/ledger] higher)
- **Possible cause:** [state the most likely reason without fabricating]
- **Suggested action:** [specific resolution step]

---

## ⚠️ Unmatched — Bank Only

Transactions present in the bank statement with no corresponding ledger entry.

| # | Date | Description | Amount | Bank Status |
|---|---|---|---|---|
| 1 | YYYY-MM-DD | [description] | $X,XXX.XX | [status field value] |

For each: state whether a receipt or note exists in context, and suggest next action.

---

## ⚠️ Unmatched — Ledger Only

Ledger entries with no corresponding bank transaction.

| # | Entry ID | Date | Description | Amount | Account |
|---|---|---|---|---|---|
| 1 | LED-XXXX | YYYY-MM-DD | [description] | $X,XXX.XX | [account] |

For each: state the most likely reason (timing, cash transaction, error) and suggest next action.

---

## ⚠️ Requires Review

Records matched on date and description but with uncertainty (date offset, pre-flagged, or low-confidence match).

| # | Date | Description | Amount | Reason for Review |
|---|---|---|---|---|
| 1 | YYYY-MM-DD | [description] | $X,XXX.XX | [specific reason] |

---

## ✅ Matched Transactions

Full matched register — every confirmed match listed.

| Bank Date | Description | Amount | Type | Ledger Entry ID | Match Basis |
|---|---|---|---|---|---|
| YYYY-MM-DD | [description] | $X,XXX.XX | debit/credit | LED-XXXX | [reference / exact / description] |

---

## Net Reconciliation Position

| Item | Amount |
|---|---|
| Bank closing balance | $X,XXX.XX |
| Ledger net change (credits − debits) | $X,XXX.XX |
| Total mismatch variances | $X,XXX.XX |
| Total bank-only unmatched | $X,XXX.XX |
| Total ledger-only unmatched | $X,XXX.XX |
| **Unreconciled difference** | **$X,XXX.XX** |

**Status:** RESOLVED (difference = $0.00) | UNRESOLVED — adjusting entries required

---

## Recommended Adjusting Entries

List only entries that are clearly required based on confirmed findings. Do not fabricate.

1. [Description of required entry] — $X,XXX.XX — [account to debit] / [account to credit]
```

## CRITICAL: What This Agent Must NOT Do

- Do NOT modify, overwrite, or delete any source files (`Bank Statement March Clean.csv`, `Internal Ledger March.csv`, `Reconciliation Notes.md`)
- Do NOT invent causes or resolutions — only state what is supported by the data
- Do NOT treat `Reconciliation Notes.md` conclusions as final — re-derive independently and note where results agree or differ
- Do NOT drop any record — every bank and ledger row must appear in the output with a status
- Do NOT round amounts when computing variances — preserve full precision
- Do NOT produce a report that is inconsistent with the computed totals

## Troubleshooting

### Bank and ledger counts differ significantly
**Cause:** Cash transactions, internal journal entries, or inter-account transfers appear in only one source
**Solution:** Classify all unmatched items correctly as BANK ONLY or LEDGER ONLY. Do not force matches.

### Same merchant appears multiple times on the same date
**Cause:** Multiple transactions with same vendor on same day (e.g., two FedEx shipments)
**Solution:** Match by amount first, then reference number. If both amount and reference match for only one, leave the second unmatched and flag as REQUIRES_REVIEW.

### Reconciliation Notes conflict with re-derived results
**Cause:** Notes were prepared manually and may reflect a different dataset version
**Solution:** State the conflict explicitly: `Note claims [X]; re-derived result is [Y]. Using re-derived result.`

### Description text differs significantly between bank and ledger
**Cause:** Bank uses payment processor names (e.g., "ADP Payroll Services") while ledger uses business names (e.g., "Payroll - biweekly")
**Solution:** Match on amount + date when descriptions are near-synonyms. Note the description difference in the Match Basis column.

## Quality Checklist

Before finalizing output, verify:

- [ ] Every bank record has a status (MATCHED, MISMATCH, REQUIRES_REVIEW, or BANK ONLY)
- [ ] Every ledger entry has a status (MATCHED, MISMATCH, REQUIRES_REVIEW, or LEDGER ONLY)
- [ ] Count of all classified records equals total bank + total ledger records
- [ ] All variances in the Net Reconciliation Position sum correctly
- [ ] No source file has been modified
- [ ] Output saved to `Data/Output/Reconciliation Report March.md`
- [ ] Recommended adjusting entries are supported by evidence in the data
- [ ] Reconciliation Notes agreements and conflicts are explicitly stated
