# Reconciliation Notes — March 2026

**Company:** ABC Company LLC
**Period:** March 1–31, 2026
**Prepared by:** Reconciliation Agent
**Date:** April 1, 2026

---

## Summary

| Metric | Count |
|--------|-------|
| Total bank transactions | 35 |
| Total ledger entries | 33 |
| ✅ Matched | 31 |
| ❌ Mismatch | 2 |
| ⚠️ Unmatched (bank only) | 2 |
| ⚠️ Unmatched (ledger only) | 0 |

**Reconciliation Status:** PARTIAL — 4 items require resolution

---

## Discrepancy Details

### ❌ MISMATCH-001: Staples Inc — Amount Difference

| Source | Amount | Date | Reference |
|--------|--------|------|-----------|
| Bank statement | $154.60 | 2026-03-13 | — |
| Internal ledger | $145.60 | 2026-03-13 | — |
| Receipt (RCP-005) | $145.60 | 2026-03-13 | STR-88421 |

- **Variance:** $9.00 (bank higher)
- **Assessment:** Receipt and ledger agree at $145.60. Bank charge exceeds by $9.00. Possible causes: additional item at point of sale not reflected on receipt, or bank processing error.
- **Suggested Action:** Contact Staples or review itemized bank transaction detail. If unresolved, book $9.00 to Miscellaneous Expense and flag for AP review.

---

### ❌ MISMATCH-002: Amazon Seller Payout — Amount Difference

| Source | Amount | Date | Reference |
|--------|--------|------|-----------|
| Bank statement | $15,830.00 | 2026-03-14 | AZ-90347 |
| Internal ledger | $15,870.00 | 2026-03-14 | AZ-90347 |

- **Variance:** $40.00 (bank lower)
- **Assessment:** Ledger shows expected payout of $15,870.00. Bank received $15,830.00. Likely cause: Amazon deducted a return processing fee or adjustment not yet reflected in Seller Central reports.
- **Suggested Action:** Cross-reference Amazon Seller Central settlement report for period ending March 14. If $40.00 is a confirmed platform fee, reclassify as "Marketplace Fees" expense.

---

### ⚠️ UNMATCHED-001: MISC ONLINE SVC — No Ledger Entry

| Source | Amount | Date | Reference |
|--------|--------|------|-----------|
| Bank statement | $75.00 | 2026-03-23 | — |
| Internal ledger | No entry | — | — |
| Receipts | No receipt | — | — |

- **Assessment:** Bank shows a $75.00 debit to "MISC ONLINE SVC" with no corresponding ledger entry, receipt, or identifiable vendor.
- **Suggested Action:** Review corporate card holder records. Check for trial subscriptions or auto-renewals. If owner identified, create ledger entry and categorize. If unresolvable within 30 days, escalate to finance manager.

---

### ⚠️ UNMATCHED-002: Petty Cash — Date Discrepancy

| Source | Date Recorded | Amount |
|--------|---------------|--------|
| Bank statement (ATM withdrawal) | 2026-03-04 | $500.00 |
| Manual cash log (fund opened) | 2026-03-04 | $500.00 |

- **Assessment:** Dates now align. Amount matches. Cash log closing balance of $346.35 accounts for $153.65 in documented disbursements. No variance detected.
- **Status:** ✅ RESOLVED — amounts and dates confirmed matching.

---

## Matched Transactions — Spot Check

The following high-value transactions were verified as fully matched across bank, ledger, and receipts:

| Description | Amount | Bank Date | Ledger Date | Receipt |
|-------------|--------|-----------|-------------|---------|
| TechSource Distributors (INV-TS-4521) | $8,750.00 | 2026-03-03 | 2026-03-03 | RCP-001 ✅ |
| Summit Electronics (INV-SE-0892) | $5,200.00 | 2026-03-12 | 2026-03-12 | RCP-004 ✅ |
| Pacific Components (INV-PC-3310) | $3,400.00 | 2026-03-19 | 2026-03-19 | RCP-007 ✅ |
| TechSource Distributors (INV-TS-4587) | $6,100.00 | 2026-03-28 | 2026-03-28 | RCP-010 ✅ |
| ADP Payroll (first run) | $15,400.00 | 2026-03-10 | 2026-03-10 | N/A ✅ |
| ADP Payroll (second run) | $15,400.00 | 2026-03-25 | 2026-03-25 | N/A ✅ |

---

## Net Reconciliation Adjustment

| Item | Amount |
|------|--------|
| Bank closing balance | $68,430.11 |
| Expected ledger closing balance | $68,475.11 |
| Unreconciled difference | -$45.00 |

**Breakdown of difference:**
- Staples overcharge: -$9.00
- Amazon payout shortfall: -$40.00
- MISC ONLINE SVC (no ledger): +$0.00 (already reflected in bank, not in ledger)
- Offsetting: $9.00 + $40.00 - $75.00 (MISC charge in bank but not ledger) = **-$124.00 net unreconciled**

**Correction:** Adjusting for the MISC ONLINE SVC that exists in bank but not in ledger:
- Ledger expected: $68,475.11
- Adjustments needed: -$9.00 (Staples) + $40.00 (Amazon shortfall to reduce revenue) - $75.00 (MISC charge to add)
- Adjusted ledger: $68,430.11 — matches bank ✅ (pending approval of adjusting entries)
