# SQL Practice Lab

Interactive SQL lessons using the Olist Brazilian E-Commerce dataset and Supabase PostgreSQL. Learn the material, run the included read-only queries, and try your own answers in the Mini-Test.

First time here? Follow [Supabase setup](SUPABASE_SETUP_README.md) to create a database and import the data.

To host one shared, read-only course database on Vercel, follow [Vercel deployment](VERCEL_DEPLOYMENT.md).

## Start the site

Install the dependencies once:

```bash
python -m pip install -r requirements.txt
```

Then open the launcher for your system:

| macOS | Windows |
| --- | --- |
| Double-click `Open_SQL_Tutorial_Mac.command` | Double-click `Open_SQL_Tutorial_Windows.bat` |

The site opens at <http://127.0.0.1:8765>. Keep the Terminal or server window open while using live queries.

If the launcher does not work, run `python sql_tutorial_server.py` and open that address yourself. Do not open `sql_tutorial.html` with `file:///`; the lessons will display, but queries cannot run.

### Windows note

The Windows launcher works with a project-local `.venv`, Miniforge in its default location, or Python on your PATH. If Python is not installed, install [Miniforge](https://github.com/conda-forge/miniforge/releases/latest) or [Python](https://www.python.org/downloads/windows/), then run the install command above.

## Connect Supabase

1. In Supabase, select **Connect** → **Session pooler** and copy the connection string on port **5432**.
2. In the site sidebar, open **Connect your Supabase database**.
3. Paste the URL, enter your database password separately, and select **Test connection**.

Leave Supabase's `[YOUR-PASSWORD]` placeholder in the copied URL; enter the real password only in the password field. Copy the pooler host exactly—do not construct it yourself.

For a class fallback connection, ask a TA for the password and use the course URL they provide. Never put a password in this repository or a shared document.

### Course fallback connection

If you have trouble connecting to Supabase, use the course connection below and ask a TA for the database password:

```text
postgresql://postgres.zwvlipptpuwndregtgzv:[YOUR-PASSWORD]@aws-0-ca-central-1.pooler.supabase.com:5432/postgres
```

Paste the URL unchanged into **Session pooler URL**, then enter the password from the TA in the separate **Database password** field.

## Use the lessons

- Use the sidebar to navigate Fundamentals, Advanced SQL, Mini-Test, and Appendix.
- Select **Show SQL**, then **Run SQL**, to execute an example.
- In Mini-Test, write a query under **Try your SQL** and select **Run my SQL**.
- The Appendix contains copyable table-management examples for use in the Supabase SQL Editor.

The local server permits only `SELECT`, `WITH`, and `EXPLAIN`; all write and schema-changing statements are rejected. The Appendix examples are intentionally copy-only.

## Troubleshooting

| Problem | Check |
| --- | --- |
| `Failed to fetch` | The local server is running and you opened `http://127.0.0.1:8765`, not a `file:///` URL. |
| URL/host error | Re-copy **Connect → Session pooler** URL on port 5432 without editing it. |
| Cannot connect | Confirm the Supabase project is active, then re-enter the database password. |
| Site is not connected | Select **Test connection** before running SQL. |

Visit <http://127.0.0.1:8765/api/health> to confirm that the local server is available. If diagrams fail to load, force-refresh the page.

## Security

The server listens only on `127.0.0.1`; passwords stay in its memory and are not written to disk. Reset a Supabase password immediately if it is exposed.

## Project files

| File | Purpose |
| --- | --- |
| `sql_tutorial.html` | Tutorial frontend |
| `sql_tutorial_server.py` | Local read-only query server |
| `SUPABASE_SETUP_README.md` | Supabase and dataset setup |
| `VERCEL_DEPLOYMENT.md` | Shared course database deployment and shutdown |
| `requirements.txt` | Python dependencies |
