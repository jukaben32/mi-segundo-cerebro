# Category Rules — ABC Company LLC

**Version:** 1.2
**Last Updated:** March 15, 2026
**Maintained by:** Finance Team

---

## Revenue Categories

| Category | Subcategory | Matching Rules | Examples |
|----------|-------------|----------------|----------|
| Revenue | Marketplace Sales | Description contains "Amazon Seller Payout" or "eBay Managed Payments" | Amazon deposits, eBay deposits |
| Revenue | Direct Sales | Description contains "Shopify Payout" | Shopify store revenue |

---

## Expense Categories

| Category | Subcategory | Matching Rules | Examples |
|----------|-------------|----------------|----------|
| COGS | Inventory Purchases | Vendor in [TechSource Distributors, Summit Electronics, Pacific Components] | Bulk product orders |
| COGS | Shipping & Freight | Vendor in [FedEx, UPS, USPS] and amount > $100 | Outbound shipments, freight |
| Operating Expenses | Rent & Facilities | Description contains "Rent" or "Commercial Properties" | Office/warehouse lease |
| Operating Expenses | Utilities | Vendor in [Austin Energy, City of Austin, AT&T] | Electric, water, internet |
| Operating Expenses | Office Supplies | Vendor in [Staples, Office Depot, Best Buy] or description contains "supplies" | Paper, toner, organizers |
| Operating Expenses | Software & Subscriptions | Vendor in [Shopify Inc, Intuit QuickBooks] and description contains "Subscription" | SaaS tools |
| Operating Expenses | Insurance | Vendor contains "State Farm" or "Insurance" | Business insurance |
| Marketing & Advertising | Digital Advertising | Vendor in [Google Ads, Meta Platforms] | PPC campaigns, social ads |
| Payroll | Salaries & Wages | Description contains "ADP Payroll" | Biweekly payroll runs |
| Travel & Transport | Rideshare | Description contains "Uber" or "Lyft" | Client visit transportation |
| Travel & Transport | Parking | Description contains "Parking" or "Garage" | Parking fees |
| Meals & Entertainment | Team Meals | Description contains "Lunch" or vendor in [Chipotle, Panera Bread] | Team lunches |
| Meals & Entertainment | Client Meals | Description contains "client" and ("coffee" or "meeting") | Client meetings |
| Miscellaneous | Postage | Vendor contains "USPS" and amount < $100 | Stamps, small parcels |
| Miscellaneous | Petty Cash | Description contains "ATM" or "Cash Withdrawal" | Cash fund replenishment |
| Uncategorized | Unknown | No matching rule found | Requires manual review |

---

## Confidence Scoring

| Confidence | Criteria |
|------------|----------|
| **high** | Exact vendor match + amount pattern consistent with history |
| **medium** | Partial description match or first-time vendor with clear category keywords |
| **low** | Ambiguous description, no vendor match, or conflicting signals |

---

## Rules of Application

1. Apply rules top-to-bottom; first match wins
2. If multiple categories could apply, use the more specific subcategory
3. Transactions under $50 from unknown vendors → assign "Miscellaneous" with `medium` confidence
4. Any transaction flagged `REQUIRES_REVIEW` by the Data Cleaner retains that flag regardless of categorization confidence
5. Never override a human-assigned category during re-processing
