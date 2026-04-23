# ── BUSINESS ANALYST EDA ─────────────────────────────────────────────
# Goal: Answer key business questions around revenue, geography,
# payments, fulfilment, and regulatory risk to drive strategic decisions

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── LOAD DATA ─────────────────────────────────────────────────────────
combined = pd.read_csv('pharma_combined.csv')

# Data prep
combined['unit_price_usd'] = pd.to_numeric(combined['unit_price_usd'], errors='coerce')
combined['quantity']       = pd.to_numeric(combined['quantity'], errors='coerce')
combined['total_revenue']  = combined['quantity'] * combined['unit_price_usd']
combined['order_date']     = pd.to_datetime(combined['order_date'], errors='coerce')
combined['month']          = combined['order_date'].dt.to_period('M')
combined['sales_tax_rate'] = combined['sales_tax_rate'].str.replace('%', '').astype(float) / 100

# ══════════════════════════════════════════════════════════════════════
# 1. REVENUE PERFORMANCE
# Business question: Is the business growing and at what rate?
# ══════════════════════════════════════════════════════════════════════

# Headline metrics — the first numbers a stakeholder wants to see
print("=== REVENUE SUMMARY ===")
print(f"Total Revenue:         ${combined['total_revenue'].sum():,.2f}")
print(f"Average Order Value:   ${combined['total_revenue'].mean():,.2f}")
print(f"Max Order Value:       ${combined['total_revenue'].max():,.2f}")
print(f"Min Order Value:       ${combined['total_revenue'].min():,.2f}")

# Monthly revenue — shows growth trend over time
monthly_revenue = combined.groupby('month')['total_revenue'].sum()

# Month over month growth rate — tells us if we are accelerating or slowing down
# pct_change() calculates the % difference between each month and the one before it
mom_growth = monthly_revenue.pct_change() * 100

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
# ax1 and ax2 are two separate chart areas stacked vertically
# this lets us show revenue and growth rate side by side in one image

# Top chart — revenue trend
monthly_revenue.plot(ax=ax1, color='steelblue', linewidth=2)
ax1.set_title('Monthly Revenue Trend')
ax1.set_xlabel('Month')
ax1.set_ylabel('Revenue ($)')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
# FuncFormatter customises the y axis tick labels to show $ and commas

# Bottom chart — growth rate
mom_growth.plot(ax=ax2, color='green', linewidth=2)
ax2.axhline(y=0, color='red', linestyle='--')
# axhline draws a horizontal reference line at 0
# bars above = growth, bars below = decline
ax2.set_title('Month over Month Revenue Growth %')
ax2.set_xlabel('Month')
ax2.set_ylabel('Growth %')

plt.tight_layout()
plt.savefig('revenue_trend.png')
plt.show()

# ══════════════════════════════════════════════════════════════════════
# 2. DRUG PORTFOLIO ANALYSIS
# Business question: Which drugs drive profit vs which just drive volume?
# ══════════════════════════════════════════════════════════════════════

top_drugs_volume  = combined.groupby('drug')['order_id'].count().sort_values(ascending=False).head(10)
top_drugs_revenue = combined.groupby('drug')['total_revenue'].sum().sort_values(ascending=False).head(10)

# Average revenue per order by drug — identifies pricing opportunities
# A low average on a high volume drug suggests it may be underpriced
avg_revenue_per_drug = combined.groupby('drug')['total_revenue'].mean().sort_values(ascending=False).head(10)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 8))
# Three charts side by side for easy comparison

# Volume chart
sns.barplot(x=top_drugs_volume.values, y=top_drugs_volume.index, color='steelblue', ax=ax1)
for i, v in enumerate(top_drugs_volume.values):
    ax1.text(v, i, f' {v:,.0f}', va='center')
ax1.set_title('Top 10 by Order Volume')
ax1.set_xlabel('Number of Orders')

# Revenue chart
sns.barplot(x=top_drugs_revenue.values, y=top_drugs_revenue.index, color='steelblue', ax=ax2)
for i, v in enumerate(top_drugs_revenue.values):
    ax2.text(v, i, f' ${v:,.0f}', va='center')
ax2.set_title('Top 10 by Total Revenue')
ax2.set_xlabel('Total Revenue ($)')

# Average revenue per order chart — the pricing insight
sns.barplot(x=avg_revenue_per_drug.values, y=avg_revenue_per_drug.index, color='steelblue', ax=ax3)
for i, v in enumerate(avg_revenue_per_drug.values):
    ax3.text(v, i, f' ${v:,.0f}', va='center')
ax3.set_title('Top 10 by Avg Revenue per Order')
ax3.set_xlabel('Avg Revenue ($)')

plt.suptitle('Drug Portfolio Analysis', fontsize=16, fontweight='bold')
# suptitle adds one master title above all three charts
plt.tight_layout()
plt.savefig('drug_portfolio.png')
plt.show()

# ══════════════════════════════════════════════════════════════════════
# 3. GEOGRAPHIC MARKET ANALYSIS
# Business question: Where should we focus sales efforts?
# ══════════════════════════════════════════════════════════════════════

state_revenue = combined.groupby('state_name')['total_revenue'].sum().sort_values(ascending=False)
state_volume  = combined.groupby('state_name')['order_id'].count().sort_values(ascending=False)

# Pareto analysis — what % of revenue comes from top states
# In most businesses 20% of customers drive 80% of revenue
total_rev     = state_revenue.sum()
cumulative    = state_revenue.cumsum() / total_rev * 100
# cumsum() adds up values progressively so we can see when we hit 80%
states_for_80 = cumulative[cumulative <= 80].count()
print(f"\n{states_for_80} states drive 80% of total revenue")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# Top 15 states by revenue
sns.barplot(x=state_revenue.head(15).values,
            y=state_revenue.head(15).index,
            color='steelblue', ax=ax1)
for i, v in enumerate(state_revenue.head(15).values):
    ax1.text(v, i, f' ${v:,.0f}', va='center')
ax1.set_title('Top 15 States by Revenue')
ax1.set_xlabel('Total Revenue ($)')

# Bottom 15 states — untapped markets
sns.barplot(x=state_revenue.tail(15).values,
            y=state_revenue.tail(15).index,
            color='salmon', ax=ax2)
# salmon colour to visually distinguish underperforming markets
ax2.set_title('Bottom 15 States by Revenue\n(Potential Untapped Markets)')
ax2.set_xlabel('Total Revenue ($)')

plt.suptitle('Geographic Market Analysis', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('geographic_analysis.png')
plt.show()

# ══════════════════════════════════════════════════════════════════════
# 4. PAYMENT & COLLECTIONS RISK
# Business question: What is our collections risk?
# ══════════════════════════════════════════════════════════════════════

payment_counts  = combined['payment_method'].value_counts()
payment_revenue = combined.groupby('payment_method')['total_revenue'].sum().sort_values(ascending=False)

# Missing payment info — orders we may not be able to collect on
missing_payment = combined['payment_method'].isnull().sum()
missing_pct     = missing_payment / len(combined) * 100
print(f"\n=== COLLECTIONS RISK ===")
print(f"Orders with missing payment info: {missing_payment} ({missing_pct:.1f}%)")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Payment method distribution
sns.barplot(x=payment_counts.values, y=payment_counts.index, color='steelblue', ax=ax1)
for i, v in enumerate(payment_counts.values):
    ax1.text(v, i, f' {v:,.0f}', va='center')
ax1.set_title('Orders by Payment Method')
ax1.set_xlabel('Number of Orders')

# Revenue by payment method — shows which channels drive the most value
sns.barplot(x=payment_revenue.values, y=payment_revenue.index, color='steelblue', ax=ax2)
for i, v in enumerate(payment_revenue.values):
    ax2.text(v, i, f' ${v:,.0f}', va='center')
ax2.set_title('Revenue by Payment Method')
ax2.set_xlabel('Total Revenue ($)')

plt.suptitle('Payment & Collections Analysis', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('payment_analysis.png')
plt.show()

# ══════════════════════════════════════════════════════════════════════
# 5. ORDER FULFILMENT ANALYSIS
# Business question: Where are we losing orders?
# ══════════════════════════════════════════════════════════════════════

status_counts = combined['order_status'].value_counts()
cancel_rate   = combined[combined['order_status'] == 'Cancelled'].shape[0] / len(combined) * 100
# shape[0] gives the row count of the filtered dataframe
print(f"\n=== FULFILMENT SUMMARY ===")
print(f"Cancellation Rate: {cancel_rate:.1f}%")

# Cancellations by state — identifies if problem is regional
cancel_by_state = combined[combined['order_status'] == 'Cancelled']\
    .groupby('state_name')['order_id'].count()\
    .sort_values(ascending=False).head(10)
# The \ lets you continue code on the next line for readability

# Cancellations by drug
cancel_by_drug = combined[combined['order_status'] == 'Cancelled']\
    .groupby('drug')['order_id'].count()\
    .sort_values(ascending=False).head(10)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 8))

# Overall status breakdown
sns.barplot(x=status_counts.values, y=status_counts.index, color='steelblue', ax=ax1)
for i, v in enumerate(status_counts.values):
    ax1.text(v, i, f' {v:,.0f}', va='center')
ax1.set_title('Order Status Breakdown')
ax1.set_xlabel('Number of Orders')

# Cancellations by state
sns.barplot(x=cancel_by_state.values, y=cancel_by_state.index, color='salmon', ax=ax2)
ax2.set_title('Top 10 States by Cancellations')
ax2.set_xlabel('Cancelled Orders')

# Cancellations by drug
sns.barplot(x=cancel_by_drug.values, y=cancel_by_drug.index, color='salmon', ax=ax3)
ax3.set_title('Top 10 Drugs by Cancellations')
ax3.set_xlabel('Cancelled Orders')

plt.suptitle('Order Fulfilment Analysis', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('fulfilment_analysis.png')
plt.show()

# ══════════════════════════════════════════════════════════════════════
# 6. REGULATORY RISK BY STATE
# Business question: Are we over-exposed in high risk states?
# ══════════════════════════════════════════════════════════════════════

# Group revenue by regulatory tier
# Tier 1 = lenient, Tier 2 = moderate, Tier 3 = strict
reg_revenue = combined.groupby('regulatory_tier')['total_revenue'].sum()
reg_volume  = combined.groupby('regulatory_tier')['order_id'].count()

# Revenue at risk = revenue coming from tier 3 (strictest) states
tier3_revenue = reg_revenue.get(3, 0)
tier3_pct     = tier3_revenue / combined['total_revenue'].sum() * 100
# .get(3, 0) safely gets tier 3 value, returns 0 if it doesn't exist
print(f"\n=== REGULATORY RISK ===")
print(f"Revenue from Tier 3 states: ${tier3_revenue:,.2f} ({tier3_pct:.1f}% of total)")

# Top tier 3 states by revenue — specific states to monitor
tier3_states = combined[combined['regulatory_tier'] == 3]\
    .groupby('state_name')['total_revenue'].sum()\
    .sort_values(ascending=False).head(10)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Revenue by regulatory tier
colors = ['green', 'orange', 'red']
# green for low risk, orange for medium, red for high
sns.barplot(x=reg_revenue.index.astype(str), y=reg_revenue.values,
            palette=colors, ax=ax1)
for i, v in enumerate(reg_revenue.values):
    ax1.text(i, v, f' ${v:,.0f}', ha='center')
ax1.set_title('Revenue by Regulatory Tier')
ax1.set_xlabel('Regulatory Tier (1=Low Risk, 3=High Risk)')
ax1.set_ylabel('Total Revenue ($)')

# Top tier 3 states
sns.barplot(x=tier3_states.values, y=tier3_states.index, color='salmon', ax=ax2)
for i, v in enumerate(tier3_states.values):
    ax2.text(v, i, f' ${v:,.0f}', va='center')
ax2.set_title('Top Tier 3 States by Revenue\n(Highest Regulatory Risk)')
ax2.set_xlabel('Total Revenue ($)')

plt.suptitle('Regulatory Risk Analysis', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('regulatory_risk.png')
plt.show()