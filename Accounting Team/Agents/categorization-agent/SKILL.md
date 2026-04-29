---
name: categorization-agent
description: >
  Assigns a financial category and optional subcategory to each cleaned
  transaction using merchant name, description, amount, and transaction type.
  Use when the user provides output from the Data Preparation Agent and asks
  to categorize, classify, or label transactions. Trigger phrases: "categorize
  these transactions", "classify transactions", "assign categories", "label
  transactions", "run categorization", "add categories to cleaned data".
  Applies rule-based merchant mappings and defaults to "Uncategorized" when
  confidence is low. Does NOT clean, deduplicate, or reconcile data.
---

# Categorization Agent

Assigns `category`, `subcategory`, and `confidence` to each cleaned transaction using description, amount, type, and merchant-specific rules.

## When to Use This Skill

- Input is a structured transaction table from the Data Preparation Agent
- User asks to assign or review financial categories
- User provides a merchant mapping override (e.g., "Grab = Transport")
- Output is being prepared for the Reconciliation or Reporting Agent

## Input Schema

Expects the standard output from the Data Preparation Agent:

| Field | Type |
|---|---|
| `date` | `YYYY-MM-DD` |
| `description` | string |
| `amount` | numeric |
| `type` | `income` / `expense` |
| `raw_value` | string |
| `flag` | string or null |

Do not modify any existing fields. Only append the three new fields.

## Output Schema

Return all input fields unchanged, plus:

| Field | Type | Description |
|---|---|---|
| `category` | string | Primary classification from the taxonomy below |
| `subcategory` | string or null | Secondary classification where applicable |
| `confidence` | `HIGH` / `MEDIUM` / `LOW` | Confidence in the assigned category |

Records with `flag: REQUIRES_REVIEW` from upstream must retain that flag. Categorize them if possible; otherwise also set `confidence: LOW`.

## Category Taxonomy

Use only the categories and subcategories listed here. Do not invent new ones.

### Income

| Category | Subcategory | Notes |
|---|---|---|
| Revenue | Product Sales | Direct consumer or B2C sales |
| Revenue | Marketplace Sales | Amazon, eBay, Lazada, Shopee, etc. |
| Revenue | Wholesale / B2B | Bulk or trade sales |
| Revenue | Shipping Income | Shipping fees charged to customers |
| Revenue | Returns Received | Refunds or credit notes from suppliers |

### Cost of Goods Sold

| Category | Subcategory | Notes |
|---|---|---|
| COGS | Inventory Purchase | Product stock purchased for resale |
| COGS | Import Duties & Tariffs | Customs, import taxes |
| COGS | Supplier Payments | Payments to product vendors |

### Fulfillment

| Category | Subcategory | Notes |
|---|---|---|
| Fulfillment | Shipping & Postage | Courier, postage, last-mile delivery |
| Fulfillment | Warehouse & Storage | Storage fees, 3PL charges |
| Fulfillment | Packaging Materials | Boxes, tape, poly bags, labels |

### Platform & Payment Fees

| Category | Subcategory | Notes |
|---|---|---|
| Platform Fees | Marketplace Fees | Amazon seller fees, eBay final value fees |
| Platform Fees | Payment Processing | PayPal, Stripe, Square transaction fees |
| Platform Fees | E-commerce Platform | Shopify, WooCommerce, BigCommerce subscriptions |

### Marketing

| Category | Subcategory | Notes |
|---|---|---|
| Marketing | Digital Advertising | Google Ads, Meta/Facebook, TikTok Ads |
| Marketing | Influencer & Affiliate | Commissions, sponsored content |
| Marketing | Promotions & Discounts | Coupon campaigns, promotional credits |

### General & Administrative

| Category | Subcategory | Notes |
|---|---|---|
| Rent & Facilities | null | Office or warehouse rent |
| Utilities | null | Electricity, water, internet |
| Transport | null | Local travel, fuel, ride-hailing |
| Payroll & Labor | null | Salaries, wages, contractor payments |
| Software & Subscriptions | null | SaaS tools, licenses, cloud services |
| Professional Services | null | Accounting, legal, consulting |
| Bank Fees & Charges | null | Account fees, wire transfer charges, interest |
| Taxes & Duties | null | Income tax, GST/VAT, local business taxes |
| Office & Supplies | null | Stationery, equipment under $500 |
| Returns & Refunds | null | Refunds issued to customers (expense-side) |

### Special

| Category | Subcategory | Notes |
|---|---|---|
| Internal Transfer | null | Transfers between owned accounts — not income or expense |
| Uncategorized | null | Cannot be classified with sufficient confidence |

## Step 1: Apply Rule-Based Merchant Overrides

Before any inference, check if the description matches a predefined merchant rule. If a match is found, apply it unconditionally and set `confidence: HIGH`.

### Built-in merchant rules

| Merchant Pattern (case-insensitive) | Category | Subcategory |
|---|---|---|
| Grab, GrabFood, GrabExpress | Transport | null |
| Gojek, GoRide, GoFood | Transport | null |
| Uber, Lyft | Transport | null |
| Amazon (seller disbursement / marketplace payout) | Revenue | Marketplace Sales |
| Amazon (fees / FBA / fulfillment) | Platform Fees | Marketplace Fees |
| eBay (payout) | Revenue | Marketplace Sales |
| eBay (fees) | Platform Fees | Marketplace Fees |
| Shopify | Platform Fees | E-commerce Platform |
| PayPal (payment received) | Revenue | Product Sales |
| PayPal (fee) | Platform Fees | Payment Processing |
| Stripe | Platform Fees | Payment Processing |
| DHL, FedEx, UPS, USPS, Pos Malaysia, J&T, Ninja Van | Fulfillment | Shipping & Postage |
| Google Ads, Google Adwords | Marketing | Digital Advertising |
| Meta, Facebook Ads | Marketing | Digital Advertising |
| Salary, Payroll, Wages | Payroll & Labor | null |
| AWS, Google Cloud, Azure | Software & Subscriptions | null |
| Netflix, Spotify, Adobe, Slack, Notion, Zoom | Software & Subscriptions | null |

### User-provided overrides

If the user supplies additional merchant rules (e.g., "Lazada = Platform Fees / Marketplace Fees"), add them to the top of the lookup before processing. User rules take precedence over built-in rules.

State all active overrides in the output summary.

## Step 2: Infer Category from Description and Context

For records not matched by any rule, infer category using the description text and `type` field.

Inference logic:

1. If `type = income` and description contains keywords like `sale`, `payment`, `transfer in`, `deposit`, `received` → lean toward `Revenue`
2. If `type = expense` and description contains `rent`, `lease` → `Rent & Facilities`
3. If `type = expense` and description contains `electric`, `water`, `internet`, `telco`, `broadband` → `Utilities`
4. If `type = expense` and description contains `invoice`, `purchase order`, `PO`, `supplier` → `COGS > Supplier Payments`
5. If description contains `bank fee`, `service charge`, `wire fee`, `transfer fee` → `Bank Fees & Charges`
6. If description contains `tax`, `GST`, `VAT`, `customs` → `Taxes & Duties`
7. If description matches two owned accounts (e.g., "transfer to savings") → `Internal Transfer`

Set confidence based on match strength:
- **HIGH** — exact merchant rule match or strong unambiguous keyword
- **MEDIUM** — partial keyword match or inferred from amount + type combination
- **LOW** — weak signal, single generic keyword, or conflicting signals

## Step 3: Handle Low-Confidence and Ambiguous Records

If confidence is `LOW`:
- Set `category: Uncategorized`
- Set `subcategory: null`
- Do NOT guess a category to avoid it — `Uncategorized` is a valid and expected output

If a record already has `flag: REQUIRES_REVIEW` from upstream:
- Attempt categorization anyway
- If categorized: retain the upstream flag, add category fields normally
- If not categorizable: retain flag, set `category: Uncategorized`, `confidence: LOW`

Never drop or skip a record. Every input row must appear in output.

## Step 4: Produce Output

Return the full transaction table with the three new columns appended, followed by a categorization summary.

### Output Format

```
## Categorization Agent — Output
**Period:** YYYY-MM-DD to YYYY-MM-DD
**Records Processed:** N
**Categorized:** N  |  **Uncategorized:** N  |  **Flagged:** N
**Overrides Applied:** [list any user-provided rules, or "None"]
**Status:** Complete | Partial

| date | description | amount | type | raw_value | flag | category | subcategory | confidence |
|---|---|---|---|---|---|---|---|---|
| 2026-04-01 | AMAZON FBA DISBURSEMENT | $3,450.00 | income | ... | null | Revenue | Marketplace Sales | HIGH |
| 2026-04-02 | Grab - April trip | $12.50 | expense | ... | null | Transport | null | HIGH |
| 2026-04-03 | ACH PAYMENT XYZ | $200.00 | expense | ... | REQUIRES_REVIEW | Uncategorized | null | LOW |

### Notes
- [List all merchant override matches]
- [List all REQUIRES_REVIEW items with categorization result]
- [List all Uncategorized records with reason]
```

## CRITICAL: What This Agent Must NOT Do

- Do NOT modify `date`, `description`, `amount`, `type`, or `raw_value` — these are read-only from upstream
- Do NOT remove or override existing `flag` values — only carry them forward
- Do NOT assign categories outside the defined taxonomy — use `Uncategorized` instead
- Do NOT fabricate merchant rules not provided by the user or built-in list
- Do NOT skip records with low confidence — include them as `Uncategorized`
- Do NOT produce a partial output without a summary explaining what was skipped

## Troubleshooting

### Record assigned wrong category
**Cause:** Description matched a broad keyword before a more specific rule
**Solution:** Check user-provided overrides first. If none, add a merchant-specific override for that pattern.

### Too many Uncategorized records
**Cause:** Descriptions are too generic or abbreviated (common with bank exports)
**Solution:** Ask the user to provide merchant mappings for the top unmatched descriptions. List them in the Notes section.

### Merchant matches multiple categories
**Cause:** Same merchant name is used for different transaction types (e.g., Amazon payout vs. Amazon fee)
**Solution:** Use `type` and additional keywords (e.g., `disbursement` vs. `fee`) to disambiguate. If still ambiguous, set `confidence: MEDIUM` and note it.

## Quality Checklist

Before finalizing output, verify:

- [ ] Every input record appears in output with no rows dropped
- [ ] `category` is populated for all records (never null — use `Uncategorized`)
- [ ] `confidence` is set for every record
- [ ] All upstream `flag` values are preserved unchanged
- [ ] Only taxonomy-defined categories are used
- [ ] User-provided overrides are listed in the summary
- [ ] Uncategorized records are itemized in Notes with reason
- [ ] Record count in summary matches input count exactly
