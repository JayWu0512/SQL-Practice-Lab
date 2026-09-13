# Create Your Supabase SQL Demo Project

This guide creates a personal Supabase PostgreSQL database for the SQL Practice Lab. It is separate from the project README so you can follow it once, then return to the tutorial.

> Never share your database password, full connection string with a password inserted, service-role key, or personal access token in GitHub, Canvas, Slack, or screenshots.

## What You Will Create

By the end, you will have:

- a free Supabase account;
- an organization that holds your projects;
- a PostgreSQL project named something like `SQL Demo - Jane Doe`;
- a database password saved privately; and
- a Session pooler URL that works with the SQL Practice Lab.

## 1. Create a Supabase Account

1. Go to [Supabase Dashboard](https://supabase.com/dashboard/sign-up).
2. Sign up with GitHub, Google, or email.
3. Verify your email if Supabase asks you to do so.
4. Return to the Supabase Dashboard and sign in.

## 2. Create an Organization

An organization is a workspace that contains one or more Supabase projects.

1. In the dashboard, open the organization switcher in the upper-left corner.
2. Select **New organization**. Some dashboard versions may label this **Create organization**.
3. Enter an organization name. Example:

   ```text
   IDS720 SQL Practice
   ```

4. Choose the **Free** plan if it is available and appropriate for your work.
5. Finish creating the organization.

## 3. Create a New Project

1. Inside the new organization, select **New project**.
2. Complete the project form using values similar to these:

   | Field | Suggested value |
   | --- | --- |
   | Organization | `IDS720 SQL Practice` (or your own organization) |
   | Project name | `SQL Demo - Your Name` |
   | Database password | Create a long, unique password and save it in a password manager. |
   | Region | Choose the region closest to you or your class. For this course, `Canada (Central)` is a reasonable example when available. |
   | Plan | Free, unless your instructor gives different instructions. |

3. Select **Create new project**.
4. Wait until provisioning finishes. The project dashboard will open when the database is ready.

### Important: Save the Database Password

The database password is different from your Supabase login password. Keep it private. You will enter it later into the SQL Practice Lab's local connection form. If you forget it, reset it in the Supabase Dashboard instead of asking someone to recover it for you.

## 4. Optional: Explore the Database Tools

Your project now includes a PostgreSQL database.

- **Table Editor** lets you view tables and rows visually.
- **SQL Editor** lets you run SQL directly in the Supabase Dashboard.
- **Database** contains database settings and tools.

You do not need to create tables before opening the SQL Practice Lab. Follow your course instructions for loading data or using the course demo database.

## 5. Copy the Correct Connection URL

The SQL Practice Lab runs as a local, persistent Python server. To work reliably on typical student networks, use the **Session pooler** connection string on port **5432**.

1. Open your Supabase project dashboard.
2. Click **Connect** near the top of the page.
3. Choose **Session pooler**.
4. Keep the connection-string format selected.
5. Copy the complete URL. It will resemble this:

   ```text
   postgresql://postgres.PROJECT_REF:[YOUR-PASSWORD]@POOLER_HOST:5432/postgres
   ```

6. Do not guess or manually assemble `POOLER_HOST`. Copy it from the Connect dialog exactly.

For this tutorial, do **not** use the Transaction pooler URL on port `6543`. Do not use a Direct connection URL if your network cannot reach IPv6.

Supabase documents the connection choices and explains that the Session pooler uses port `5432`; see [Connect to your database](https://supabase.com/docs/guides/database/connecting-to-postgres).

## 6. Connect It to SQL Practice Lab

1. Start this project using `Open_SQL_Tutorial_Mac.command` on macOS or `Open_SQL_Tutorial_Windows.bat` on Windows.
2. In the website sidebar, open **Connect your Supabase database**.
3. Paste the copied Session pooler URL into **Session pooler URL**. You may leave `[YOUR-PASSWORD]` exactly as Supabase copied it.
4. Enter your real database password in the separate **Database password** field.
5. Select **Test connection**.
6. A green **Connected to Supabase** message means the connection is ready.

The website keeps the password only in the local server process while it is running. It does not write the password into the HTML file, the URL, or this repository.

## 7. Manually Upload the Included Olist CSV Files

This repository includes `data/data.zip`. It contains the four CSV files used by the tutorial:

| Table | CSV file | Primary key | Rows after import |
| --- | --- | --- | ---: |
| `customers` | `customers.csv` | `customer_id` | 99,441 |
| `orders` | `orders.csv` | `order_id` | 99,441 |
| `products` | `products.csv` | `product_id` | 32,951 |
| `order_items` | `order_items.csv` | `(order_id, order_item_id)` | 112,650 |

You will create each table directly from its CSV file in Supabase Table Editor. No Python import program is needed.

1. In the cloned project folder, unzip `data/data.zip`. On macOS, double-click it. On Windows, right-click it and choose **Extract All**.
2. In the Supabase Dashboard, open **Table Editor** and select **New table**.

   <img src="assets/06-new-table-import-csv.png" alt="Supabase new-table screen with the Import data from CSV button" width="900">

3. Select **Import data from CSV**, then choose `customers.csv` from the unzipped folder.
4. Supabase previews the column names, detected types, and row count. Check that `customer_id` is a `text` column and has the Primary checkbox selected.

   <img src="assets/07-csv-import-column-preview.png" alt="Supabase CSV preview showing customer_id selected as the primary key" width="900">

5. Set the table name to `customers`, then save the table. The preview should show 99,441 rows and five columns.

   <img src="assets/08-name-table-and-confirm-primary-key.png" alt="Supabase create-table screen named customers with imported CSV columns" width="900">

6. Repeat the same process for the remaining files. Ensure that the listed single-column primary key is checked before saving:

   | CSV file | Table name | Primary key to select |
   | --- | --- | --- |
   | `products.csv` | `products` | `product_id` |
   | `orders.csv` | `orders` | `order_id` |
   | `order_items.csv` | `order_items` | Clear any single-column primary key (including a default `id` column, if shown); follow the composite-key step below. |

7. After all four tables appear in Table Editor, your list should look similar to this:

   <img src="assets/05-table-editor-existing-tables.png" alt="Supabase Table Editor listing customers, order_items, orders, and products" width="602">

### Set the `order_items` Composite Primary Key

One order can contain more than one item, so `order_id` alone is not unique. After importing `order_items.csv`, open **SQL Editor** → **New query**, paste the following SQL, and select **Run**:

~~~sql
ALTER TABLE order_items
ADD CONSTRAINT order_items_pkey PRIMARY KEY (order_id, order_item_id);
~~~

This is the only required SQL step in the manual-upload workflow. It adds the correct two-column primary key without changing any uploaded rows.

After each upload, check the row count in Table Editor. The expected counts are listed in the table above.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `failed to resolve host` or a host-related error | Re-copy the complete **Session pooler** URL from **Connect**. Do not type the pooler host yourself. |
| The host “does not appear to be an IPv4 or IPv6 address” | Keep `[YOUR-PASSWORD]` in the URL field and put the real password only in the separate password field. |
| Connection fails after copying a URL | Confirm that it is **Session pooler** and port **5432**, then re-enter the database password. |
| The SQL Practice Lab says it is not connected | Select **Test connection** before using a Run SQL button. |
| You forgot the password | Reset the database password in the Supabase Dashboard. Do not share passwords with classmates. |

## Next Step

Return to the main [README.md](README.md) to start the SQL Practice Lab and run your first query.
