# Additional Mini-Tests

These exercises use the current Olist tables: `customers`, `orders`, `order_items`, and `products`.

## Mini-Test 1 — Basic aggregation

The `customers` table contains one row per customer record. Return the 10 cities with the most customer records. Sort from the largest customer count to the smallest.

**Output:** `customer_city`, `customer_count`

### Answer key

```sql
SELECT
    customer_city,
    COUNT(*) AS customer_count
FROM customers
GROUP BY customer_city
ORDER BY customer_count DESC, customer_city
LIMIT 10;
```

## Mini-Test 2 — JOIN and aggregation

Find the five product categories with the highest item revenue from delivered orders. Only include rows with a known product category, and calculate revenue from `order_items.price` only—do not include freight.

**Output:** `product_category_name`, `total_revenue`

### Answer key

```sql
SELECT
    p.product_category_name,
    ROUND(SUM(oi.price)::numeric, 2) AS total_revenue
FROM orders AS o
JOIN order_items AS oi
    ON o.order_id = oi.order_id
JOIN products AS p
    ON oi.product_id = p.product_id
WHERE o.order_status = 'delivered'
  AND p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY total_revenue DESC, p.product_category_name
LIMIT 5;
```

## Mini-Test 3 — Second transaction

The `customers` table maps each `customer_id` to a persistent `customer_unique_id`. Return every customer’s second order in chronological order. When two purchase timestamps are the same, use `order_id` to break the tie. Exclude customers with fewer than two orders.

**Output:** `customer_unique_id`, `order_id`, `order_purchase_timestamp`

### Answer key

```sql
WITH ranked_orders AS (
    SELECT
        c.customer_unique_id,
        o.order_id,
        o.order_purchase_timestamp,
        ROW_NUMBER() OVER (
            PARTITION BY c.customer_unique_id
            ORDER BY o.order_purchase_timestamp, o.order_id
        ) AS order_number
    FROM customers AS c
    JOIN orders AS o
        ON c.customer_id = o.customer_id
)
SELECT
    customer_unique_id,
    order_id,
    order_purchase_timestamp
FROM ranked_orders
WHERE order_number = 2
ORDER BY order_purchase_timestamp, order_id;
```
