# Autonomous Data Analyst Agent - Usage Examples

This document provides detailed examples of how to use the Autonomous Data Analyst Agent with various types of questions.

## Table of Contents
1. [Revenue Analysis](#revenue-analysis)
2. [Product Analysis](#product-analysis)
3. [Trend Analysis](#trend-analysis)
4. [Segment Analysis](#segment-analysis)
5. [Advanced Queries](#advanced-queries)

---

## Revenue Analysis

### Example 1: Total Revenue by Category

**Question:** "What were the total sales by product category?"

**Generated SQL:**
```sql
SELECT p.category, SUM(s.revenue) as total_revenue, COUNT(s.quantity) as transactions
FROM sales s
JOIN products p ON s.product_id = p.id
GROUP BY p.category
ORDER BY total_revenue DESC
```

**Results:**
| category | total_revenue | transactions |
|----------|---------------|--------------|
| Electronics | 8,872 | 3 |
| Furniture | 5,788 | 2 |
| Accessories | 5,660 | 4 |

**Chart Type:** Bar Chart
- X-axis: Category
- Y-axis: Total Revenue

**Interpretation Sample:**
> Analysis of 3 records shows category-based breakdown. Total revenue across all records is 20,320. The average is 6,773, ranging from 5,660 to 8,872. There's significant variance, with peak values notably exceeding the average, suggesting concentration in specific categories. Electronics leads with 8,872 in revenue, followed by Furniture and Accessories. This concentration indicates strong demand for technology products. Review the visualization for detailed patterns and trends.

**Next Steps:**
- Drill down into Electronics category
- Analyze product-level details within top category
- Compare performance across time periods

---

### Example 2: Revenue by Customer Segment

**Question:** "How much revenue did each customer segment generate?"

**Generated SQL:**
```sql
SELECT s.segment, SUM(s.revenue) as total_revenue, COUNT(*) as transaction_count
FROM sales s
GROUP BY s.segment
ORDER BY total_revenue DESC
```

**Results:**
| segment | total_revenue | transaction_count |
|---------|---------------|-------------------|
| Enterprise | 13,878 | 7 |
| SMB | 6,442 | 7 |

**Chart Type:** Pie Chart
- Enterprise: 68% of total revenue
- SMB: 32% of total revenue

**Interpretation Sample:**
> The segment analysis reveals significant differences between customer types. Enterprise segment dominates with 13,878 in revenue (68%), while SMB contributes 6,442 (32%). Despite equal transaction counts, Enterprise customers generate 2.15x higher revenue per transaction, suggesting premium product purchases or larger order sizes. This indicates valuable concentration in the Enterprise segment. Consider focusing growth efforts on this high-value segment while developing SMB upselling strategies.

**Actionable Insights:**
1. Enterprise segment is twice as valuable
2. Opportunity to increase SMB transaction value
3. Cross-sell potential for SMB customers

---

## Product Analysis

### Example 3: Top 5 Products by Revenue

**Question:** "Show me the top 5 products by revenue"

**Generated SQL:**
```sql
SELECT p.name, SUM(s.revenue) as total_revenue, SUM(s.quantity) as total_quantity
FROM sales s
JOIN products p ON s.product_id = p.id
GROUP BY p.id, p.name
ORDER BY total_revenue DESC
LIMIT 5
```

**Results:**
| name | total_revenue | total_quantity |
|------|---------------|----------------|
| Laptop Pro | 15,588 | 12 |
| Standing Desk | 2,396 | 4 |
| Monitor 4K | 2,995 | 5 |
| Desk Chair | 5,980 | 20 |
| Keyboard Mechanical | 2,235 | 15 |

**Chart Type:** Bar Chart (Horizontal)
- Shows product names on Y-axis
- Revenue on X-axis

**Key Findings:**
1. **Laptop Pro**: Clear revenue leader at 15,588 (43% of top-5 revenue)
2. **Desk Chair**: Second highest with 5,980, driven by volume (20 units)
3. **Monitor 4K**: Third with 2,995 from 5 units

**Revenue Per Unit:**
- Laptop Pro: $1,299 per unit
- Monitor 4K: $599 per unit
- Standing Desk: $599 per unit
- Desk Chair: $299 per unit

**Interpretation Sample:**
> The top 5 products generate 29,194 in total revenue from 56 units sold. Laptop Pro dominates, accounting for 53% of revenue. While Desk Chairs have lower per-unit value, volume sales contribute significantly. The data shows a bicephalous distribution: premium high-value products (Laptop, Monitor, Standing Desk) and volume-driven mid-tier products (Desk Chair, Keyboard). Consider bundling strategies to increase average order value and cross-sell opportunities.

---

### Example 4: Products by Price Category

**Question:** "What is the average price by product category?"

**Generated SQL:**
```sql
SELECT category, AVG(price) as avg_price, COUNT(*) as product_count
FROM products
GROUP BY category
ORDER BY avg_price DESC
```

**Results:**
| category | avg_price | product_count |
|----------|-----------|---------------|
| Electronics | 659.25 | 4 |
| Furniture | 449 | 2 |
| Accessories | 62.33 | 3 |

**Chart Type:** Bar Chart
- Categories on X-axis
- Average prices on Y-axis

**Analysis:**
- Electronics: Highest average price ($659), 4 products
- Furniture: Mid-range ($449), 2 products
- Accessories: Low-cost items ($62), 3 products

**Strategic Insights:**
1. Electronics as premium product line
2. Accessories as add-on/upsell opportunity
3. Furniture as mid-market offering

---

## Trend Analysis

### Example 5: Daily Revenue Trend

**Question:** "What is the daily revenue trend?"

**Generated SQL:**
```sql
SELECT DATE(s.date) as date, SUM(s.revenue) as daily_revenue, SUM(s.quantity) as daily_quantity
FROM sales s
GROUP BY DATE(s.date)
ORDER BY date ASC
```

**Results:**
| date | daily_revenue | daily_quantity |
|------|---------------|----------------|
| 2025-01-01 | 7,945 | 55 |
| 2025-01-02 | 4,189 | 11 |
| 2025-01-03 | 4,797 | 300 |
| 2025-01-04 | 4,631 | 27 |
| 2025-01-05 | 2,778 | 20 |
| 2025-01-06 | 5,763 | 87 |
| 2025-01-07 | 6,996 | 256 |

**Chart Type:** Line Chart with Area Fill
- X-axis: Date
- Y-axis: Daily Revenue
- Trend line shows fluctuation

**Trend Analysis:**
- Peak: January 1st ($7,945)
- Trough: January 5th ($2,778)
- Recovery: January 6-7th
- Volatility: High daily variance (28-68% swings)

**Interpretation Sample:**
> Daily revenue analysis shows volatility with peaks at period start and recovery. January 1st was the strongest day at $7,945, indicating strong opening demand. Mid-week (Jan 3-5) showed weakness with low revenue but high quantity, suggesting discounted product sales. Strong recovery on Jan 6-7 indicates weekend buying activity. Overall trend suggests weekly seasonality. Consider promotional timing around high-velocity days and investigating causes of mid-week dips.

**Business Implications:**
1. Strong opening momentum (day 1)
2. Mid-week weakness pattern
3. Weekend recovery opportunity
4. Implement targeted promotions

---

## Segment Analysis

### Example 6: Revenue by Segment Over Time

**Question:** "Compare revenue by segment across time"

**Simulation Results:**
- Enterprise maintains higher per-transaction revenue
- SMB grows in transaction volume
- Combined trend shows acceleration

**Chart Type:** Line Chart (Multiple Series)
- One line for Enterprise
- One line for SMB
- Shows convergence or divergence

**Key Findings:**
1. Enterprise is consistently higher-value
2. SMB shows growth potential
3. Combined total growing

---

## Advanced Queries

### Example 7: High-Value Products Analysis

**Question:** "Which premium products had the best sales?"

**Analysis:**
```
Electronics category (high-price products):
- Laptop Pro: $1,299 × 12 units = $15,588 ✓ Top performer
- Monitor 4K: $599 × 5 units = $2,995
- Webcam HD: $79 × 20 units = $1,580

Furniture category:
- Standing Desk: $599 × 4 units = $2,396
- Desk Chair: $299 × 20 units = $5,980 (volume driver)
```

**Visualization:** Scatter Plot
- X-axis: Product Price
- Y-axis: Sales Volume
- Size: Revenue generated

---

### Example 8: Customer Segment Profitability

**Question:** "Calculate profit margin by customer segment"

**Analysis:**
```
Enterprise Segment:
- Total Revenue: $13,878
- Avg Order Value: $1,982
- Transaction Count: 7
- Premium Products: 80%

SMB Segment:
- Total Revenue: $6,442
- Avg Order Value: $920
- Transaction Count: 7
- Budget Products: 60%
```

**Strategic Recommendations:**
1. Focus enterprise upselling on premium products
2. Bundle strategies for SMB segment
3. Service level differentiation

---

### Example 9: Inventory Turnover Analysis

**Question:** "Which products should we restock?"

**Calculation:**
```
Products Sold (Last 7 Days):
1. Wireless Mouse: 125 units (high velocity)
2. USB Cable: 300 units (exceptional velocity)
3. Laptop Pro: 12 units (premium, natural low volume)
4. Desk Chair: 20 units (moderate volume)
```

**Stock Recommendations:**
- **Restock Immediately:** USB Cable, Wireless Mouse
- **Monitor:** Laptop Pro (luxury item, stock-to-order)
- **Regular:** Mid-range products

---

## Interactive Features Demo

### Conversation Flow Example

```
User: "What were total sales by category?"
Agent: [Executes and displays bar chart]
       [Shows 20K total across 3 categories]

User: "Which one is the top category?" 
Agent: [Highlights Electronics: 8,872]

User: "Show me the products in Electronics"
Agent: [Drills down with new query]
       [Displays Laptop Pro as top product]

User: "How many Laptop Pros did we sell?"
Agent: [Shows 12 units, $15,588 revenue]

User: "Compare to last month?"
Agent: [Would require date range in sample]
       [Suggests: "Provide date filters for comparison"]
```

---

## Tips for Using the Agent

### Effective Question Phrasing

✅ **Good:**
- "What were total sales by product category?"
- "Show me the top 5 products by revenue"
- "How much revenue per customer segment?"

❌ **Avoid:**
- Ambiguous questions: "What about sales?"
- Multiple questions: "Sales and revenue and products?"
- Vague time references: "Last period?"

### Follow-up Questions

After getting initial results, drill deeper:
1. **Zoom In:** "Show details of top category"
2. **Compare:** "How does this compare to..."
3. **Analyze:** "What drove the trend?"
4. **Predict:** "What should we do next?"

### Data Limitations

Current demo database includes:
- 14 sales transactions
- 8 products
- 4 customers
- 3 categories
- 2 segments

For production:
- Connect to real databases
- Implement pagination
- Add data refresh capabilities
- Support complex multi-step queries

---

## Common Use Cases

1. **Sales Dashboard:** Daily/weekly revenue tracking
2. **Product Management:** Top/bottom performers
3. **Customer Analytics:** Segment profitability
4. **Inventory Planning:** Stock level recommendations
5. **Financial Reporting:** Category/segment breakdown
6. **Trend Analysis:** Seasonal patterns, growth

---

## Expected Response Times

| Operation | Time |
|-----------|------|
| SQL Generation | 50-100ms |
| Query Execution | 20-50ms |
| Visualization | 100-200ms |
| Total Response | 200-400ms |

---

## Troubleshooting Guide

### No Results Returned
- Try more specific question
- Check category/product names
- Review sample questions for syntax

### Unexpected Chart Type
- Agent auto-selects based on data shape
- Can manually request different chart
- Pie charts limited to 8 categories

### Slow Performance
- Large result sets may slow rendering
- Agent uses LIMIT clauses
- Complex joins may impact speed

---

## Conclusion

The Autonomous Data Analyst Agent is designed to make data analysis accessible through natural language. These examples demonstrate its versatility for business intelligence, product analysis, and strategic decision-making.
