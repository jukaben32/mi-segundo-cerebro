# Reconciliation Report — March 2026

**Company:** ABC Company LLC
**Period:** 2026-03-01 – 2026-03-31
**Sources:** Bank Statement March Clean, Internal Ledger March, Reconciliation Notes
**Prepared:** 2026-04-03

---

## Summary

| Metric | Count |
|--------|-------|
| Bank transactions | 35 |
| Ledger entries | 34 |
| ✅ Matched | 31 |
| ❌ Mismatches | 2 |
| ⚠️ Bank-only (missing from ledger) | 1 |
| ⚠️ Ledger-only (missing from bank) | 0 |
| Duplicates detected | 0 |

**Status: PARTIAL — 3 items require resolution**

> **Note:** Prior reconciliation notes (Reconciliation Notes.md) state 33 ledger entries. Current ledger file contains 34 entries. Difference is the petty cash entry (LED-0304-001), which was previously flagged as unmatched but is now present and resolved. Counts above reflect the current file state.

---

## ❌ Mismatches

### MISMATCH-001 — Staples Inc | 2026-03-13

| Source | Amount | Reference |
|--------|--------|-----------|
| Bank statement | $154.60 | — |
| Internal ledger (LED-0313-001) | $145.60 | — |
| Receipt (RCP-005) | $145.60 | STR-88421 |

- **Variance:** $9.00 (bank higher)
- **Reason:** Receipt and ledger agree at $145.60. Bank charged $9.00 more. Possible causes: additional item at point of sale not on receipt, or bank processing error.
- **Action required:** Obtain itemized bank transaction detail or contact Staples to verify. If confirmed overcharge, dispute with vendor. If confirmed additional purchase, update ledger to $154.60 and obtain amended receipt. If unresolvable, book $9.00 to Miscellaneous Expense.

---

### MISMATCH-002 — Amazon Seller Payout (Ref AZ-90347) | 2026-03-14

| Source | Amount | Reference |
|--------|--------|-----------|
| Bank statement | $15,830.00 | AZ-90347 |
| Internal ledger (LED-0314-001) | $15,870.00 | AZ-90347 |

- **Variance:** $40.00 (bank lower)
- **Reason:** Ledger recorded expected payout of $15,870.00; bank received $15,830.00. Likely cause: Amazon deducted a return processing fee or platform adjustment not yet reflected in Seller Central reports.
- **Action required:** Cross-reference Amazon Seller Central settlement report for the period ending 2026-03-14. If the $40.00 is a confirmed platform fee or deduction, correct ledger to $15,830.00 and book $40.00 as Marketplace Fees expense (LED-0314-001 update + new entry).

---

## ⚠️ Missing Entries

### MISSING-001 — MISC ONLINE SVC | 2026-03-23 | Bank only

| Source | Amount | Reference |
|--------|--------|-----------|
| Bank statement | $75.00 | — |
| Internal ledger | No entry | — |
| Receipt | None | — |

- **Reason:** $75.00 debit posted to bank with no vendor identification, no corresponding ledger entry, and no receipt or reference on file.
- **Action required:** Review corporate card/account holder activity for 2026-03-23. Check for auto-renewals or trial subscriptions. If vendor identified, create ledger entry and categorize. If unresolvable within 30 days, escalate to finance manager. Currently categorized as Uncategorized in transaction data.

---

## Duplicates

No duplicate transactions detected across bank statement or internal ledger for March 2026.

Recurring entries verified as legitimate:
- ADP Payroll ($15,400.00) — 2026-03-10 and 2026-03-25: confirmed biweekly schedule
- FedEx Shipping — 2026-03-05, 2026-03-17, 2026-03-30: different amounts, confirmed separate shipments (RCP-002, RCP-006, RCP-011)
- UPS Freight — 2026-03-07 and 2026-03-24: different amounts and references (TRK-112233445, TRK-556677889)
- Google Ads — 2026-03-05 and 2026-03-26: separate campaign billing cycles
- Meta Platforms — 2026-03-14 and 2026-03-31: separate billing cycles

---

## ✅ Matched Transactions (31)

| Date | Description | Amount | Direction |
|------|-------------|--------|-----------|
| 2026-03-01 | Westfield Commercial Properties - Rent | $3,200.00 | Debit |
| 2026-03-01 | Shopify Inc - Monthly Subscription | $79.00 | Debit |
| 2026-03-03 | Amazon Seller Payout - Ref AZ-90281 | $18,450.00 | Credit |
| 2026-03-03 | TechSource Distributors - INV-TS-4521 | $8,750.00 | Debit |
| 2026-03-04 | ATM Cash Withdrawal - Petty Cash Fund | $500.00 | Debit |
| 2026-03-05 | FedEx Shipping Services | $1,230.45 | Debit |
| 2026-03-05 | Google Ads - Campaign CPC | $650.00 | Debit |
| 2026-03-07 | eBay Managed Payments - Ref EB-44120 | $5,890.00 | Credit |
| 2026-03-07 | UPS Freight Charges | $980.00 | Debit |
| 2026-03-08 | Shopify Payout - Direct Sales | $3,200.00 | Credit |
| 2026-03-10 | ADP Payroll Services - Biweekly | $15,400.00 | Debit |
| 2026-03-10 | Austin Energy - Electric Utility | $420.35 | Debit |
| 2026-03-11 | AT&T Business Services | $189.99 | Debit |
| 2026-03-12 | Summit Electronics Inc - INV-SE-0892 | $5,200.00 | Debit |
| 2026-03-14 | Meta Platforms - Advertising | $800.00 | Debit |
| 2026-03-15 | State Farm Insurance - Commercial Policy | $560.00 | Debit |
| 2026-03-16 | Shopify Payout - Direct Sales | $2,800.00 | Credit |
| 2026-03-17 | FedEx Shipping Services | $890.00 | Debit |
| 2026-03-18 | City of Austin - Water Utility | $95.20 | Debit |
| 2026-03-19 | Pacific Components Inc - INV-PC-3310 | $3,400.00 | Debit |
| 2026-03-20 | eBay Managed Payments - Ref EB-44298 | $4,760.00 | Credit |
| 2026-03-21 | Intuit QuickBooks - Subscription | $45.00 | Debit |
| 2026-03-22 | Amazon Seller Payout - Ref AZ-90412 | $21,200.00 | Credit |
| 2026-03-24 | UPS Freight Charges | $1,100.00 | Debit |
| 2026-03-25 | ADP Payroll Services - Biweekly | $15,400.00 | Debit |
| 2026-03-25 | Shopify Payout - Direct Sales | $4,100.00 | Credit |
| 2026-03-26 | Google Ads - Campaign CPC | $720.00 | Debit |
| 2026-03-27 | Office Depot - Supplies | $210.30 | Debit |
| 2026-03-28 | TechSource Distributors - INV-TS-4587 | $6,100.00 | Debit |
| 2026-03-29 | Amazon Seller Payout - Ref AZ-90503 | $14,340.00 | Credit |
| 2026-03-30 | FedEx Shipping Services | $670.00 | Debit |
| 2026-03-31 | Meta Platforms - Advertising | $550.00 | Debit |

---

## Net Balance Impact

| Item | Bank | Ledger | Variance |
|------|------|--------|----------|
| Opening balance | $45,230.00 | $45,230.00 | $0.00 |
| Closing balance (actual / implied) | $68,430.11 | $68,554.11 | -$124.00 |

**Variance breakdown:**

| Issue | Effect on Ledger vs Bank |
|-------|--------------------------|
| MISMATCH-001: Staples overcharge (+$9.00 in bank) | Ledger understates expenses by $9.00 → ledger balance overstated by $9.00 |
| MISMATCH-002: Amazon payout shortfall (-$40.00 in bank) | Ledger overstates revenue by $40.00 → ledger balance overstated by $40.00 |
| MISSING-001: MISC ONLINE SVC ($75.00 in bank, not in ledger) | Ledger missing $75.00 expense → ledger balance overstated by $75.00 |
| **Total unreconciled** | **+$124.00 (ledger overstated)** |

Pending the three adjusting entries above, ledger closing balance adjusts from $68,554.11 to **$68,430.11** — matching bank. ✅
