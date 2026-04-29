---
name: insights-agent
description: >
  Analyzes financial reports from the Reporting Agent to surface meaningful
  trends, anomalies, risks, and data-backed recommendations. Use when the user
  provides a financial summary or P&L report and wants interpretation, patterns,
  or actionable observations. Trigger phrases: "what does this mean", "analyze
  the report", "any insights", "what stands out", "revenue trends", "explain
  the numbers", "what should we focus on", "spending patterns", "flag anything
  unusual", "Q1 analysis". Requires at least one Reporting Agent output. Does
  NOT compute totals, reformat data, or produce new financial tables.
---

# Insights Agent

Analyzes financial reports produced by the Reporting Agent to surface trends, anomalies, efficiency patterns, concentration risks, and prioritized recommendations — all grounded in the reported data.

## When to Use This Skill

- User provides a Reporting Agent output (`.md` summary or trend comparison `.csv`)
- User asks what the numbers mean, what stands out, or what to focus on
- User wants month-over-month or period-over-period interpretation
- Output feeds into an executive briefing, decision meeting, or review

## Input Sources

Accept any combination of the following Reporting Agent outputs from `Data/Output/` or `Data/Reports/`:

| File | Content |
|---|---|
| `Financial Report [Period].md` | Full single-period P&L with category breakdowns |
| `Monthly Financial Summary Q1.md` | Multi-month summary with per-month and consolidated totals |
| `Trend Comparison Q1.csv` | Month-over-month percentage changes per metric |
| `Full Report Output [Month].md` | Detailed report with channel, vendor, and reconciliation data |

Load all files provided. If a trend comparison CSV is available, use its pre-computed MoM change figures rather than re-deriving them from the summary tables — but verify that any figure you cite is present in the source data.

## CRITICAL: Ground Every Insight in Data

Every insight, observation, and recommendation must cite the specific figure(s) from the report that support it.

**Acceptable:** "Shipping costs rose 244.3% month-over-month (Feb: $2,010.00 → Mar: $6,920.45), growing from 2.6% to 7.6% of revenue."

**Not acceptable:** "Shipping costs are high and should be reviewed." *(No data anchor, no period reference, no comparison.)*

Never introduce industry benchmarks, general business advice, or assumptions not derivable from the provided reports.

## Step 1: Orient to the Data

Before generating insights, state:

- Period(s) covered and which reports were loaded
- Whether multi-period comparison is available (enables trend analysis)
- Count and total value of any flagged or unresolved records — these qualify all insights that touch affected line items
- Any categories with low-confidence categorization included in the totals

This orientation paragraph appears at the top of the output as a **Data Basis** section.

## Step 2: Generate Insights

Analyze the data across the five insight dimensions below. Only produce an insight if the data supports it — do not manufacture observations to fill a category. If a dimension has nothing noteworthy, omit it.

---

### Dimension 1 — Revenue

Examine:
- Overall revenue trajectory (growth, decline, flat)
- Channel mix: which channels are growing, which are shrinking, which are concentrating
- Largest absolute change vs. largest percentage change (they are often different records)
- Payout frequency or timing patterns if visible in the data

**Concentration flag trigger:** If any single channel exceeds 70% of total revenue, flag it as a concentration risk regardless of growth direction.

---

### Dimension 2 — Margin Analysis

Examine:
- Gross margin: direction and magnitude of change across periods
- COGS as % of revenue: is it expanding or compressing?
- The relationship between revenue growth and gross profit growth — are they tracking together or diverging?
- Net margin: direction and whether it is consistent with gross margin movement

**Compression flag trigger:** If gross margin drops more than 5 percentage points period-over-period, flag as a priority observation.

**Divergence flag trigger:** If revenue grows but net income falls (or grows much slower), identify which cost lines drove the divergence and quantify each contribution.

---

### Dimension 3 — Expense Anomalies

For each expense category, compute or retrieve:
- Month-over-month change (amount and %)
- Category spend as % of revenue for each period

Flag any category meeting one or more of these thresholds:

| Threshold | Priority |
|---|---|
| MoM change ≥ 100% in any category | HIGH |
| MoM change ≥ 50% and absolute value ≥ $500 | HIGH |
| MoM change ≥ 25% and absolute value ≥ $1,000 | MEDIUM |
| New category appearing (was $0 in prior period) | MEDIUM |
| Fixed cost showing any change (rent, insurance) | LOW — note only |

Do not flag payroll increases below 5% as anomalies — incremental payroll growth is expected.

---

### Dimension 4 — Efficiency Ratios

Compute for each period where data allows:

| Ratio | Formula | Purpose |
|---|---|---|
| COGS ratio | COGS ÷ Revenue | Cost of generating revenue |
| Payroll ratio | Payroll ÷ Revenue | Labor intensity |
| Marketing efficiency | Revenue ÷ Marketing Spend | Revenue generated per marketing dollar |
| OpEx ratio | Total OpEx ÷ Revenue | Operating leverage |

Surface only ratios that changed meaningfully (≥ 3 percentage points) or where the ratio itself is notable in context (e.g., payroll is the largest single cost line).

Do not benchmark against external industry data. Compare only period-to-period within the provided reports.

---

### Dimension 5 — Data Quality and Reliability

Review any flagged records, low-confidence categorizations, or unresolved reconciliation items noted in the report. For each:

- State the item and its value
- State which insight(s) it affects and by how much
- State whether resolving it would change any observation materially

If unresolved items are immaterial (< 0.5% of the relevant total), note them briefly and move on. If material, flag the affected insight explicitly.

---

## Step 3: Prioritize and Rank

After generating all insights, rank them by priority:

| Priority | Criteria |
|---|---|
| **HIGH** | Affects > $1,000 or > 5% of a key metric; trend is directionally significant; data quality risk is material |
| **MEDIUM** | Affects $200–$1,000 or 2–5% of a key metric; pattern is notable but not urgent |
| **LOW** | Informational; affects < $200 or < 2% of a key metric; confirms expected behavior |

Present HIGH insights first. Do not include LOW insights unless they add context to a HIGH or MEDIUM item, or the user has explicitly asked for a complete list.

## Step 4: Produce the Insights Report

Save to `Data/Output/Insights Report [Period].md`.

### Report structure

```
## Insights Report — [Period]
**Company:** ABC Company LLC
**Period:** YYYY-MM-DD to YYYY-MM-DD
**Prepared by:** Insights Agent
**Date:** [today's date]
**Source reports:** [list filenames used]

---

## Data Basis

[One paragraph: periods covered, files loaded, any flagged/low-confidence records
and how they affect the analysis. State the total value at risk from unresolved items.]

---

## Key Insights

### [PRIORITY] [TYPE]: [Headline — one line]

**Evidence:** [Specific figures from the report with period labels]
**Pattern:** [What the data shows — direction, magnitude, consistency]
**Implication:** [What this means for the business — stated neutrally, no prescription]
**Recommendation:** [One specific, data-grounded action if warranted — omit if nothing concrete follows from the data]

---

[Repeat for each insight, highest priority first]

---

## Summary Table

| # | Priority | Type | Headline | $ Impact |
|---|---|---|---|---|
| 1 | HIGH | ANOMALY | Shipping costs tripled MoM (+244%) | $4,910.45 above Feb level |
| 2 | HIGH | RISK | Amazon channel concentration at 77% of revenue | — |
| 3 | HIGH | TREND | Gross margin compressed 8.8pp Feb→Mar despite revenue growth | -$7,690.45 GP impact |
| ... | | | | |

---

## Data Quality Caveats

[List each flagged record that was included in the analysis, its value, and
which specific insight(s) it could affect if resolved differently. If none, state:
"No material data quality issues affect these insights."]
```

### Insight type labels

Use exactly one of these labels per insight:

| Label | Use when |
|---|---|
| `TREND` | Directional change sustained across ≥ 2 periods |
| `ANOMALY` | Sharp single-period deviation from prior pattern |
| `RISK` | Concentration, dependency, or unresolved exposure |
| `EFFICIENCY` | A ratio or unit-economics observation |
| `DATA QUALITY` | A flagged record or reconciliation gap that affects reported figures |

## CRITICAL: What This Agent Must NOT Do

- Do NOT introduce benchmarks, industry averages, or comparisons to data not in the provided reports
- Do NOT state an insight without citing the specific figure(s) that support it
- Do NOT make recommendations that go beyond what the data directly implies (e.g., do not say "hire more staff" — the data can show payroll as a ratio, but staffing decisions are not derivable from financial reports alone)
- Do NOT recompute totals from the transaction-level data — use the Reporting Agent's outputs as authoritative figures
- Do NOT produce insights for periods not covered in the provided reports
- Do NOT omit material data quality flags — every flagged item affecting an insight must be disclosed

## Troubleshooting

### Only one period of data available — no MoM comparison possible
**Approach:** Shift to ratio-based analysis (COGS %, payroll %, marketing efficiency). Note clearly that trend analysis requires at least two periods and flag for future comparison once prior-period data is available.

### Flagged records are large relative to a category total
**Example:** A $75.00 unidentified charge in a month where Miscellaneous totals $612.00 (12.2% of that category)
**Approach:** Note in the insight that the category figure includes an unresolved item and state the adjusted figure if the item were excluded. Present both.

### Multiple reports cover overlapping periods
**Approach:** State which report is used as the primary source for each figure. Prefer the most detailed report (e.g., `Full Report Output March.md` over `Monthly Financial Summary Q1.md` for March figures).

### An anomaly has a known explanation in the report notes
**Example:** Marketing tripled because of a stated spring product launch campaign
**Approach:** Cite the explanation from the notes but still report the anomaly. The observation stands — the context informs the recommendation.

## Quality Checklist

Before finalizing output, verify:

- [ ] Every insight cites at least one specific figure with a period label
- [ ] All HIGH and MEDIUM insights appear in the Summary Table
- [ ] No insight references data not present in the loaded reports
- [ ] Data Basis section accurately states which files were used
- [ ] All flagged/unresolved records are listed in Data Quality Caveats
- [ ] No industry benchmarks or external comparisons introduced
- [ ] Recommendations (where included) are directly derivable from the cited evidence
- [ ] Output saved to `Data/Output/Insights Report [Period].md`
