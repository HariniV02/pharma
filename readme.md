# Pharma Sales Data Analysis

## Project Overview
This project simulates a real-world business analyst workflow from raw, messy data through to actionable business insights. Using a synthetic pharmaceutical sales dataset, I performed end-to-end data cleaning in SQL and exploratory data analysis in Python to answer key strategic questions around revenue performance, market geography, payment risk, and operational efficiency.

---

## Business Questions Answered
- What is the total revenue and how is it trending month over month?
- Which drugs are driving the most revenue vs the most order volume and are they the same?
- Which states represent the biggest markets and where are the untapped opportunities?
- What is the collections risk from missing or incomplete payment data?
- Where is the company losing orders and is there a pattern to cancellations?
- Is the company over-exposed in high regulatory risk states and what revenue is at stake?

---

## Dataset
Synthetic pharmaceutical sales dataset generated in Python consisting of three relational tables:

| Table | Rows | Description |
|-------|------|-------------|
| orders | 5,000 | Core transaction table — order ID, drug, quantity, price, date, status |
| payments | 120 | Payment records — method, processor, approval code, billing zip |
| states | 50 | US state reference data — abbreviation, tax rate, regulatory tier |

**Foreign key relationships:**
- `orders.payment_id` → `payments.payment_id`
- `orders.state_id` → `states.state_id`

---

## Tools Used
- **Python** — data generation and EDA (pandas, matplotlib, seaborn)
- **SQL / DBeaver** — data cleaning and transformation
- **SQLite** — local database
- **GitHub** — version control

---

## Part 1: Data Cleaning (SQL)
The raw dataset was intentionally made messy to simulate real-world data quality issues. All cleaning was performed in SQL using DBeaver.

### Issues Identified and Resolved

**Orders Table**
- Standardised inconsistent drug name casing, spacing, and typos (e.g. `LISINOPRIL 10MG`, `Lisinoprll 10mg`, `lisinopril10mg` → `Lisinopril 10mg`)
- Standardised order status values (e.g. `COMPLETED`, `Completd`, `Complete` → `Completed`)
- Converted 7 mixed date formats to a consistent `YYYY-MM-DD` standard
- Nulled out impossible dates (e.g. `2024-02-30`, `2022-13-01`)
- Removed `$` currency symbols from price column and converted to numeric
- Nulled out negative and zero price values
- Removed `ORD-` prefix from order ID column to restore pure numeric format
- Converted empty strings to NULL across all columns
- Removed duplicate rows

**Payments Table**
- Standardised payment method labels (e.g. `Insurence`, `insur.`, `INSURANCE` → `Insurance`)
- Removed invalid billing zip codes (wrong length, letters, `N/A` strings)
- Truncated approval codes restored to correct format
- Removed duplicate rows

**States Table**
- Standardised state abbreviations to uppercase
- Fixed state name casing inconsistencies
- Converted tax rates from mixed formats (decimal and percentage string) to consistent decimal format
- Nulled out impossible tax rate values
- Removed duplicate rows

### SQL Scripts
| Script | Description |
|--------|-------------|
| `clean_orders_messy.sql` | All cleaning operations for the orders table |
| `clean_payments_messy.sql` | All cleaning operations for the payments table |
| `clean_states_messy.sql` | All cleaning operations for the states table |
| `combine.sql` | JOIN query to merge all three tables into one analysis-ready table |

---

## Part 2: Exploratory Data Analysis (Python)

All EDA was performed in `pharma_eda.py` using pandas for analysis and matplotlib/seaborn for visualisation.

### Data Quality Summary
Before analysis, a completeness audit was performed across all columns. Key findings:
- Core transactional fields (`order_id`, `payment_id`, `payment_method`) were fully complete
- `processor_network` and `approval_code` had high null rates — expected, as cash and cheque payments do not generate these values
- `sales_tax_rate` had moderate nulls concentrated in a small number of states

### Analysis 1 — Revenue Performance
**Business question:** Is the business growing and at what rate?

- Calculated total revenue, average order value, and month over month growth rate
- Plotted monthly revenue trend with a growth rate overlay
- Identified periods of acceleration and decline across the 3-year window

### Analysis 2 — Drug Portfolio Analysis
**Business question:** Which drugs drive profit vs which just drive volume?

- Compared top 10 drugs by order volume vs total revenue vs average revenue per order
- Key insight: the highest volume drugs are not always the highest revenue drugs, revealing potential pricing opportunities in the portfolio

### Analysis 3 — Geographic Market Analysis
**Business question:** Where should we focus our sales efforts?

- Ranked all 50 states by revenue and order volume
- Applied Pareto analysis to identify how many states drive 80% of total revenue
- Identified bottom 15 states as potential untapped markets for targeted outreach

### Analysis 4 — Payment & Collections Risk
**Business question:** What is our collections risk?

- Broke down order volume and revenue by payment method
- Quantified the percentage of orders with missing payment information
- Identified which payment channels are most associated with high value orders

### Analysis 5 — Order Fulfilment Analysis
**Business question:** Where are we losing orders and is there a pattern?

- Calculated overall cancellation rate
- Identified whether cancellations are concentrated in specific states or specific drugs
- Flagged operational risk areas for further investigation

### Analysis 6 — Regulatory Risk Analysis
**Business question:** Are we over-exposed in high regulatory risk states?

- Cross-referenced order revenue with state regulatory tier (1=low risk, 3=high risk)
- Calculated the percentage of total revenue coming from Tier 3 states
- Identified the specific high-risk states contributing the most revenue

---

## Key Business Insights
1. **Geographic concentration risk** — a small number of states drive the majority of revenue, creating dependency risk
2. **Drug pricing opportunity** — high volume drugs with below-average revenue per order may be underpriced relative to demand
3. **Collections exposure** — a measurable percentage of orders have incomplete payment data, representing potential revenue at risk
4. **Cancellation patterns** — cancellations are not evenly distributed, pointing to specific operational or regional issues worth investigating
5. **Regulatory exposure** — a portion of revenue is concentrated in states with the strictest regulatory environments, requiring ongoing compliance monitoring

---

## Repository Structure
```
pharma/
├── pharma_eda.py                   # Full EDA script
├── README.md                       # Project documentation
│
├── cleandata/
│   ├── orders_clean.csv            # Cleaned orders table
│   ├── payments_clean.csv          # Cleaned payments table
│   ├── states_clean.csv            # Cleaned states table
│   └── pharma_combined.csv         # Final merged analysis table
│
├── messydata/
│   ├── orders_messy.csv            # Raw messy orders table
│   ├── payments_messy.csv          # Raw messy payments table
│   └── states_messy.csv            # Raw messy states table
│
└── visuals/
    ├── revenue_trend.png           # Monthly revenue and growth rate
    ├── drug_portfolio.png          # Drug volume vs revenue analysis
    ├── geographic_analysis.png     # State level market analysis
    ├── payment_analysis.png        # Payment method breakdown
    ├── fulfilment_analysis.png     # Order status and cancellations
    └── regulatory_risk.png         # Revenue by regulatory tier

```

---

## How to Run
1. Clone the repository
2. Install dependencies:
```bash
pip3 install pandas matplotlib seaborn
```
3. Run the EDA script:
```bash
python3 pharma_eda.py
```
Charts will be saved as PNG files in the same directory.