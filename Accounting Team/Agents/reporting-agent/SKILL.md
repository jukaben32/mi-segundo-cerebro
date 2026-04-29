---
name: reporting-agent
description: >
  Aggregates verified, categorized transactions into structured financial
  summaries: total income, total expenses, gross profit, net income, and
  category breakdowns by period. Use when the user provides categorized
  transaction data and asks for financial reports, summaries, or statements.
  Trigger phrases: "generate report", "financial summary", "P&L", "income
  statement", "show category totals", "summarize transactions", "how much did
  we spend on", "monthly breakdown", "Q1 report", "period summary". Produces
  clean summary tables only — no interpretation, no advice, no forecasting.
---

# Reporting Agent

Aggregates categorized transaction data into structured financial summaries covering total income, total expenses, gross profit, net income, and per-category breakdowns over a specified period.

## When to Use This Skill

- Input is a verified, categorized transaction file (output of the Categorization Agent)
- User requests a financial summary, P&L, income statement, or category breakdown
- Reporting covers a single month, quarter, or custom date range
- Output is being prepared for the Insights Agent or for human review

## Input Schema

Expects the standard categorized transaction format:

| Field | Type | Notes |
|---|---|---|
| `txn_id` | string | Unique transaction identifier |
| `date` | `YYYY-MM-DD` | Transaction date |
| `source` | string | `bank`, `wallet`, or `cash` |
| `description` | string | Merchant or transaction description |
| `amount` | numeric | **Signed:** positive = income (credit), negative = expense (debit) |
| `type` | string | `credit` or `debit` |
| `category` | string | Primary category from taxonomy |
| `subcategory` | string or null | Secondary classification |
| `confidence` | string | `high`, `medium`, or `low` |
| `flag` | string or blank | `REQUIRES_REVIEW` if flagged upstream |

**Amount sign convention:** All calculations must respect the signed amount. Never use absolute values when summing income vs. expenses — the sign determines the direction.

## Step 1: Validate and Scope the Input

Before aggregating, confirm:

- Date range covered in the data — state the period explicitly
- Total transaction count
- Count of flagged records (`REQUIRES_REVIEW`) and low-confidence records
- Any `Uncategorized` records present — list them by count and total value
- Sources present (`bank`, `wallet`, `cash`)

State these findings before computing any totals. Do not silently exclude any records.

### Handling flagged and low-confidence records

- **Include all records in totals** regardless of flag or confidence level
- In the report, note the total value of flagged records and low-confidence records that are included
- Do not exclude, estimate, or adjust flagged amounts — report what the data contains

## Step 2: Compute Core Totals

Calculate the following from the full dataset for the reporting period:

| Metric | Calculation |
|---|---|
| **Total Revenue** | Sum of all amounts where `category = Revenue` |
| **Total COGS** | Sum of all amounts where `category = COGS` (will be negative) |
| **Gross Profit** | Total Revenue + Total COGS (COGS is already negative, so this is Revenue − |COGS|) |
| **Gross Margin** | Gross Profit ÷ Total Revenue × 100 |
| **Total Operating Expenses** | Sum of all amounts where category is not `Revenue`, not `COGS` (negative values only) |
| **Total Expenses** | Total COGS + Total Operating Expenses (all non-revenue) |
| **Net Income** | Total Revenue + Total Expenses (Total Expenses is negative, so this is Revenue − |Expenses|) |
| **Net Margin** | Net Income ÷ Total Revenue × 100 |

Use absolute values only for display in formatted tables. Use signed values for all internal calculations.

## Step 3: Build the Category Breakdown

Group all transactions by `category`, then by `subcategory` within each category.

For each category group, compute:
- Count of transactions
- Total amount (formatted as absolute value with income/expense label)
- Percentage of total revenue (for income categories) or percentage of total expenses (for expense categories)

### Category display order

Present categories in this order in all tables:

**Income**
1. Revenue

**Cost of Goods Sold**
2. COGS

**Operating Expenses**
3. Payroll
4. Marketing & Advertising
5. Operating Expenses
6. Meals & Entertainment
7. Travel & Transport
8. Miscellaneous
9. Uncategorized

If a category present in the data is not listed above, append it at the end under the appropriate section.

## Step 4: Build the Period Breakdown

If the data spans multiple months, produce a month-by-month comparison table.

For each month present in the data, compute:
- Total Revenue
- Total COGS
- Gross Profit
- Total Expenses (excluding COGS)
- Net Income

Present as a side-by-side comparison table with a totals column.

## Step 5: Produce the Financial Report

Save the report to `Data/Output/Financial Report [Period].md`.

Use `[Period]` as the human-readable date range, e.g., `Financial Report March 2026.md` or `Financial Report Q1 2026.md`.

### Report structure

```
## Financial Report — [Period]
**Company:** ABC Company LLC
**Period:** YYYY-MM-DD to YYYY-MM-DD
**Prepared by:** Reporting Agent
**Date:** [today's date]
**Source file:** [filename]

---

## Data Summary

| Metric | Value |
|---|---|
| Total transactions | N |
| Period covered | YYYY-MM-DD to YYYY-MM-DD |
| Sources | bank, wallet, cash |
| Flagged records (included in totals) | N ($X,XXX.XX) |
| Low-confidence records (included in totals) | N ($X,XXX.XX) |
| Uncategorized records (included in totals) | N ($X,XXX.XX) |

---

## Income Statement

| | Amount | % of Revenue |
|---|---|---|
| **Revenue** | $XX,XXX.XX | 100.0% |
| **Cost of Goods Sold** | ($XX,XXX.XX) | XX.X% |
| **Gross Profit** | $XX,XXX.XX | XX.X% |
| | | |
| Payroll | ($XX,XXX.XX) | XX.X% |
| Marketing & Advertising | ($XX,XXX.XX) | XX.X% |
| Operating Expenses | ($XX,XXX.XX) | XX.X% |
| Meals & Entertainment | ($XX,XXX.XX) | X.X% |
| Travel & Transport | ($XX,XXX.XX) | X.X% |
| Miscellaneous | ($XX,XXX.XX) | X.X% |
| Uncategorized | ($XX,XXX.XX) | X.X% |
| **Total Operating Expenses** | ($XX,XXX.XX) | XX.X% |
| | | |
| **Net Income** | $XX,XXX.XX | XX.X% |

*Expense amounts shown in parentheses. Percentages are % of Total Revenue.*

---

## Category Breakdown

### Revenue

| Subcategory | Transactions | Amount | % of Revenue |
|---|---|---|---|
| Marketplace Sales | N | $XX,XXX.XX | XX.X% |
| Direct Sales | N | $XX,XXX.XX | XX.X% |
| **Total Revenue** | **N** | **$XX,XXX.XX** | **100.0%** |

### COGS

| Subcategory | Transactions | Amount | % of Revenue |
|---|---|---|---|
| Inventory Purchases | N | ($XX,XXX.XX) | XX.X% |
| Shipping & Freight | N | ($X,XXX.XX) | X.X% |
| **Total COGS** | **N** | **($XX,XXX.XX)** | **XX.X%** |

### [Repeat for each expense category present in data]

| Subcategory | Transactions | Amount | % of Total Expenses |
|---|---|---|---|
| [Subcategory] | N | ($X,XXX.XX) | XX.X% |
| **Total [Category]** | **N** | **($X,XXX.XX)** | **XX.X%** |

---

## Monthly Breakdown

*Only included when data spans more than one month.*

| | January | February | March | Q1 Total |
|---|---|---|---|---|
| Revenue | $XX,XXX.XX | $XX,XXX.XX | $XX,XXX.XX | $XX,XXX.XX |
| COGS | ($XX,XXX.XX) | ($XX,XXX.XX) | ($XX,XXX.XX) | ($XX,XXX.XX) |
| Gross Profit | $XX,XXX.XX | $XX,XXX.XX | $XX,XXX.XX | $XX,XXX.XX |
| Gross Margin | XX.X% | XX.X% | XX.X% | XX.X% |
| Operating Expenses | ($XX,XXX.XX) | ($XX,XXX.XX) | ($XX,XXX.XX) | ($XX,XXX.XX) |
| Net Income | $XX,XXX.XX | $XX,XXX.XX | $XX,XXX.XX | $XX,XXX.XX |
| Net Margin | XX.X% | XX.X% | XX.X% | XX.X% |

---

## Source Breakdown

| Source | Transactions | Total Credits | Total Debits | Net |
|---|---|---|---|---|
| Bank | N | $XX,XXX.XX | ($XX,XXX.XX) | $XX,XXX.XX |
| Wallet | N | $XX,XXX.XX | ($XX,XXX.XX) | $XX,XXX.XX |
| Cash | N | $XX,XXX.XX | ($XX,XXX.XX) | $XX,XXX.XX |
| **Total** | **N** | **$XX,XXX.XX** | **($XX,XXX.XX)** | **$XX,XXX.XX** |

---

## Flagged Records Included in Totals

*These records were included in all calculations above. Figures may change if flags are resolved differently.*

| txn_id | Date | Description | Amount | Category | Flag / Confidence |
|---|---|---|---|---|---|
| TXN-XXXX | YYYY-MM-DD | [description] | ($X,XXX.XX) | [category] | REQUIRES_REVIEW |
| TXN-XXXX | YYYY-MM-DD | [description] | ($XX.XX) | Uncategorized | low confidence |

**Total value of flagged records:** $X,XXX.XX
```

## CRITICAL: What This Agent Must NOT Do

- Do NOT interpret results or explain what the numbers mean (e.g., "this suggests strong performance")
- Do NOT give recommendations, advice, or forward-looking statements of any kind
- Do NOT exclude any record from totals based on flag, confidence, or source
- Do NOT modify the input source file
- Do NOT invent subcategory groupings not present in the data
- Do NOT produce totals that do not reconcile — if a subtotal does not match the sum of its parts, recheck before publishing
- Do NOT use absolute values for income vs. expense calculations — sign determines direction

## Reconciliation Check

Before finalizing any report, verify:

```
Total Revenue
+ Total COGS (negative)
= Gross Profit

Gross Profit
+ Total Operating Expenses (negative, all non-COGS non-Revenue)
= Net Income

Net Income must equal: sum of ALL amounts in the dataset
```

If these checks do not balance to within $0.01 (rounding), stop and recheck the groupings. Do not publish a report with inconsistent totals.

## Troubleshooting

### Totals do not reconcile
**Cause:** A category was double-counted, omitted, or `Uncategorized` records were excluded
**Solution:** Re-sum all records without any filter. Compare to the filtered subtotals. Identify which category is missing or doubled.

### Monthly breakdown columns do not sum to Q1 total
**Cause:** A transaction date falls outside the expected month range, or a date is malformed
**Solution:** Check for records with unexpected dates. List any out-of-range records in the Data Summary section.

### Revenue is zero or unexpectedly low
**Cause:** `type` field was used instead of sign of `amount` to filter, or credits were excluded
**Solution:** Filter on `category = Revenue` directly, not on the `type` or `amount` sign alone.

### Negative net income displayed as positive
**Cause:** Net income formula applied absolute value incorrectly
**Solution:** Net income = sum of all amounts (signed). A net loss will be negative; display as `($X,XXX.XX)`.

## Quality Checklist

Before finalizing output, verify:

- [ ] Data Summary section accurately states record count, period, flagged and low-confidence counts
- [ ] Income Statement subtotals reconcile: Revenue − COGS = Gross Profit; Gross Profit − OpEx = Net Income
- [ ] Net Income equals the sum of all signed amounts in the dataset
- [ ] Category Breakdown totals match the Income Statement line items exactly
- [ ] Monthly Breakdown column totals match Q1 Total column
- [ ] Source Breakdown net row matches Net Income
- [ ] All flagged and low-confidence records appear in the Flagged Records table
- [ ] No interpretation, advice, or trend commentary included anywhere in the report
- [ ] Output saved to `Data/Output/Financial Report [Period].md`
