# SQL Tutorial with Supabase

An interactive SQL learning website built around the Olist Brazilian E-Commerce dataset and Supabase PostgreSQL.

Students can:

- Use the left sidebar to jump to any topic.
- Study SQL Fundamentals, Advanced SQL, Mini-Test, and Appendix content.
- View, copy, and run read-only queries from SQL blocks.
- Write their own SQL below each Mini-Test question and inspect the result.
- Copy table-management and CRUD examples from the Appendix into their own Supabase SQL Editor.

## Project Files

| File | Purpose |
|---|---|
| requirements.txt | Python dependencies for the website |
| sql_tutorial.html | Website frontend |
| sql_tutorial_server.py | Local read-only Supabase API server |
| Open_SQL_Tutorial_Mac.command | One-click macOS launcher |
| Open_SQL_Tutorial_Windows.bat | One-click Windows launcher |

## Requirements

- A web browser
- Python 3.10 or later
- sqlalchemy and psycopg[binary]
- An accessible Supabase PostgreSQL project

Install all project dependencies:

~~~bash
python -m pip install -r requirements.txt
~~~

> Both launchers find the project from the launcher's own location, so they work after the repository is cloned into any folder. They use a project-local `.venv` first (if present), then the default Miniforge installation, then Python on your system PATH.

## Open the Website

### macOS

In Finder, open the project folder and double-click:

~~~text
Open_SQL_Tutorial_Mac.command
~~~

Your browser will open:

~~~text
http://127.0.0.1:8765
~~~

Keep the Terminal window open. Closing it or pressing Control + C stops live query functionality.

### Windows

In File Explorer, double-click:

~~~text
Open_SQL_Tutorial_Windows.bat
~~~

It opens your browser and a SQL Tutorial Server window. Keep the server window open while using live queries, then close it when you are done.

### Windows First-Time Setup

The recommended option is **Miniforge** because the Windows launcher automatically detects its default installation path. A project-local `.venv` or a Python installation on PATH also works.

1. Download the current Windows x86_64 installer from the official [Miniforge releases page](https://github.com/conda-forge/miniforge/releases/latest).
2. Run the installer and choose **Just Me**. Keep the default installation folder, usually C:\Users\YOUR_NAME\miniforge3, so Open_SQL_Tutorial_Windows.bat can find it automatically.
3. Keep **Create start menu shortcuts** enabled. Adding Miniforge to PATH is optional and is not required by this project.
4. Open **Miniforge Prompt** from the Windows Start menu.
5. Install the project dependencies:

~~~bat
python -m pip install -r requirements.txt
~~~

6. Verify the installation:

~~~bat
python -c "import sqlalchemy, psycopg; print('Packages are ready')"
~~~

7. Return to File Explorer and double-click Open_SQL_Tutorial_Windows.bat.

#### Alternative: Standard Python

You can instead install Python from the official [Python for Windows download page](https://www.python.org/downloads/windows/). Make sure the python command is available in Command Prompt, then run:

~~~bat
python -m pip install -r requirements.txt
~~~

After that, double-click Open_SQL_Tutorial_Windows.bat.

### Manual Start

If the one-click launcher does not work, run this in Terminal or Command Prompt:

~~~bash
python sql_tutorial_server.py
~~~

Then open:

~~~text
http://127.0.0.1:8765
~~~

Do not open the site directly with file:///.../sql_tutorial.html. You can read the content that way, but live SQL execution will not work.

## Connect to Supabase

1. In your Supabase project, click **Connect** at the top of the page.

   <img src="assets/01-open-supabase-connect.png" alt="Supabase project page with the Connect button highlighted" width="900">

2. Choose **Direct connection**, then select **Session pooler** and keep the URL connection type. The website uses port **5432**.

   <img src="assets/02-select-session-pooler.png" alt="Supabase Connect dialog showing the Session pooler option" width="900">

3. Copy the full connection string shown under **Connection string**.

   <img src="assets/03-copy-session-pooler-url.png" alt="Supabase Session pooler connection string ready to copy" width="900">

4. Open **Connect your Supabase database** in the website sidebar.
5. Paste the copied URL into **Session pooler URL**.
6. Enter the real database password in **Database password**.
7. Click **Test connection**.
8. A green **Connected to Supabase** status confirms that the local website can run queries against your database.

   <img src="assets/04-successful-connection.png" alt="SQL Tutorial sidebar showing the successful Connected to Supabase status" width="432">

You may leave Supabase's displayed [YOUR-PASSWORD] placeholder in the copied URL:

~~~text
postgresql://postgres.PROJECT_REF:[YOUR-PASSWORD]@POOLER_HOST:5432/postgres
~~~

The website automatically handles that display-only placeholder. Your real password is used only in the local password field; it is not stored in the HTML or URL.

> Copy the complete host from **Connect → Session pooler**. Do not guess a pooler host from the region, such as aws-0-..., because the pooler index can differ.

### Course Demo Connection (Fallback)

If you cannot connect to your own Supabase project during the class, you may use the course demo Session pooler URL below. Ask a TA for the current password; do not put a password in this README, GitHub, or a shared document.

~~~text
postgresql://postgres.zwvlipptpuwndregtgzv:[YOUR-PASSWORD]@aws-0-ca-central-1.pooler.supabase.com:5432/postgres
~~~

Paste the URL as shown into **Session pooler URL**, then enter the password provided by the TA in the separate **Database password** field.

## Run SQL

After connecting:

1. Click **Show SQL** on any SQL block.
2. Click **Run SQL** in the top-right corner of that block.
3. The result appears directly below the block.

To protect the database, the local server accepts only:

- SELECT
- WITH
- EXPLAIN

It rejects INSERT, UPDATE, DELETE, CREATE, DROP, and other write or structure-changing commands.

## Mini-Test

Every Mini-Test question has a **Try your SQL** editor:

1. Read the question.
2. Write your own read-only SQL.
3. Click **Run my SQL**.
4. Inspect the result before opening a Hint or Solution.

## Appendix: Table Management

The Appendix includes copyable reference SQL for:

- CREATE TABLE
- INSERT
- SELECT
- UPDATE
- DELETE
- DROP TABLE

All examples use sql_practice and do not modify Olist tables. The Appendix provides **Copy SQL** only, not a website execution button. Paste commands into your own Supabase SQL Editor and verify the table name and WHERE clause first.

## Security

- The website server listens only on local address 127.0.0.1.
- Passwords remain only in the local server process memory and are never written to disk.
- Website queries run in a read-only transaction.
- Do not put real Supabase passwords in an HTML file, GitHub repository, or chat message.
- If a password was exposed, reset the database password in Supabase immediately.

## Troubleshooting

### Failed to fetch

The website cannot reach the local server.

- Confirm that the server window is still open.
- Confirm that the browser address is http://127.0.0.1:8765.
- Confirm that the site was not opened through file:///.
- Open http://127.0.0.1:8765/api/health in your browser. A working server returns JSON.

### IPv4 / IPv6 URL format error

Restart the local server, then paste the Session pooler URL copied from Supabase without editing it. The current server automatically handles [YOUR-PASSWORD].

### Host cannot be resolved or connection failed

Confirm that the URL was copied from **Connect → Session pooler → port 5432**, rather than built manually. Check that the Supabase project is active and your network can reach Supabase.

### Mermaid syntax error on the website

Refresh the page. On macOS, use Command + Shift + R to force-refresh cached CDN resources.
