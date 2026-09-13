# Supabase Setup

Use this once to create a personal database for SQL Practice Lab and load its Olist data. Keep your database password, service-role key, and any connection string containing a real password private.

## 1. Create a project

1. Sign in or create an account at the [Supabase Dashboard](https://supabase.com/dashboard/sign-up).
2. Create an organization if needed, then select **New project**.
3. Choose a name such as `SQL Demo - Your Name`, a nearby region, and the Free plan when appropriate.
4. Create and securely save a unique database password. This is not your Supabase login password.
5. Wait for provisioning to finish.

## 2. Copy the connection URL

In the project dashboard, select **Connect** → **Session pooler**, keep the connection-string format, and copy the full URL on port **5432**:

```text
postgresql://postgres.PROJECT_REF:[YOUR-PASSWORD]@POOLER_HOST:5432/postgres
```

Do not manually assemble the host. For this project, use Session pooler—not the Transaction pooler (port 6543). Then start SQL Practice Lab, paste the URL into **Session pooler URL**, enter the real password separately, and select **Test connection**.

## 3. Import the Olist data

1. Unzip `data/data.zip` in this repository.
2. In Supabase, open **Table Editor** → **New table** → **Import data from CSV**.
3. Import each file below. Set the table name and primary key as shown.

| CSV | Table | Primary key | Expected rows |
| --- | --- | --- | ---: |
| `customers.csv` | `customers` | `customer_id` | 99,441 |
| `products.csv` | `products` | `product_id` | 32,951 |
| `orders.csv` | `orders` | `order_id` | 99,441 |
| `order_items.csv` | `order_items` | `order_id`, + `order_item_id` | 112,650 |

Check the row counts after import. You can inspect tables in Table Editor or run queries in the SQL Editor.

## If something fails

| Problem | Check |
| --- | --- |
| Host or URL error | Re-copy the complete Session pooler URL; do not edit the pooler host. |
| Connection fails | Confirm port 5432, an active project, and the correct database password. |
| Password placeholder error | Leave `[YOUR-PASSWORD]` in the URL and use the separate password field. |
| Lab is not connected | Select **Test connection** before running a query. |

Return to [README.md](README.md) to open the lab.
