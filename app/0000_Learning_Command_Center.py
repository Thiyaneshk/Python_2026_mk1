# oracle_study_dashboard.py

# 🌐 Vision Overview: “Learning Command Center”

# Imagine this structure:

# learning_app/
# │
# ├── Home.py                     ← landing page
# ├── pages/
# │   ├── 1_Oracle_Study.py
# │   ├── 2_AI_ML_Study.py
# │   ├── 3_Data_Engineering_Study.py
# │   ├── 4_About.py
# │
# ├── data/
# │   └── topics_oracle.json
# │   └── topics_ai_ml.json
# │
# └── utils/
#     └── db.py                    ← database helper (SQLite/PostgreSQL)


# ✅ Each subject (Oracle, AI/ML, etc.) lives as its own page,
# ✅ Each page has its own dashboard & progress tracker,
# ✅ All users’ progress stored in a persistent database (e.g., SQLite → upgrade later to PostgreSQL),
# ✅ Optional login system (username/password) to separate each learner’s progress.

# 🧱 Phase 1 – Multi-Page Layout (No Login Yet)

# Streamlit automatically treats every file in /pages/ as a separate page in the sidebar.
# You can reuse 95% of your existing dashboard code per topic.

# Example directory
# learning_app/
# │
# ├── Home.py
# ├── pages/
# │   ├── 1_Oracle_Study.py
# │   ├── 2_AI_ML_Study.py

# Home.py
# import streamlit as st

# st.set_page_config(page_title="Learning Command Center", layout="wide")
# st.title("🎓 Learning Command Center")

# st.markdown("""
# Welcome to your personal learning hub!  
# Choose a topic from the sidebar to begin:

# - 🏛 **Oracle PL/SQL Developer Path**
# - 🤖 **AI / Machine Learning**
# - 🧱 **Data Engineering**
# """)

# st.markdown("---")
# st.caption("Each section saves your progress locally or to the database if configured.")


# Each page (like 1_Oracle_Study.py) can be a direct copy of your current Oracle dashboard — just modularized with your new init_state() fix.

# 🧱 Phase 2 – Persistent Progress (SQLite)

# Let’s replace JSON save/load with a real database.

# utils/db.py
# import sqlite3

# DB_FILE = "learning_progress.db"

# def init_db():
#     with sqlite3.connect(DB_FILE) as conn:
#         conn.execute("""
#             CREATE TABLE IF NOT EXISTS progress (
#                 username TEXT,
#                 topic TEXT,
#                 subtopic_id TEXT,
#                 status TEXT,
#                 notes TEXT,
#                 updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 PRIMARY KEY (username, topic, subtopic_id)
#             )
#         """)

# def save_progress(username, topic, progress, notes):
#     with sqlite3.connect(DB_FILE) as conn:
#         for sid, status in progress.items():
#             note = notes.get(sid, "")
#             conn.execute("""
#                 INSERT INTO progress (username, topic, subtopic_id, status, notes)
#                 VALUES (?, ?, ?, ?, ?)
#                 ON CONFLICT(username, topic, subtopic_id)
#                 DO UPDATE SET status=excluded.status, notes=excluded.notes, updated_at=CURRENT_TIMESTAMP
#             """, (username, topic, sid, status, note))
#         conn.commit()

# def load_progress(username, topic):
#     with sqlite3.connect(DB_FILE) as conn:
#         cur = conn.execute("SELECT subtopic_id, status, notes FROM progress WHERE username=? AND topic=?", (username, topic))
#         data = cur.fetchall()
#     return {r[0]: r[1] for r in data}, {r[0]: r[2] for r in data}


# Then, in your page file:

# from utils.db import init_db, save_progress, load_progress

# USERNAME = st.text_input("Enter your name to load/save progress", value="Thiyanesh")

# init_db()
# progress, notes = load_progress(USERNAME, "Oracle PL/SQL")

# # then update st.session_state.progress = progress etc.

# if st.button("Save progress to DB"):
#     save_progress(USERNAME, "Oracle PL/SQL", st.session_state.progress, st.session_state.notes)
#     st.success("Progress saved to DB")


# Now you have per-user, persistent storage 🎉

# 🔐 Phase 3 – Add Authentication

# Later, you can add a simple login using the streamlit-authenticator
#  package:

# pip install streamlit-authenticator


# It provides:

# Secure login/logout UI

# Password hashing

# Role support

# Cookie-based sessions

# Example:

# import streamlit_authenticator as stauth

# names = ["Thiyanesh", "Guest"]
# usernames = ["thiyanesh", "guest"]
# passwords = ["oracle2024", "guest123"]
# hashed_pw = stauth.Hasher(passwords).generate()

# authenticator = stauth.Authenticate(names, usernames, hashed_pw, "app_cookie", "secret_key", cookie_expiry_days=30)
# name, authentication_status, username = authenticator.login("Login", "main")

# if authentication_status:
#     st.sidebar.success(f"Welcome {name}")
# elif authentication_status is False:
#     st.error("Username/password incorrect")
# elif authentication_status is None:
#     st.warning("Please log in")


# Then use the username to load/save progress.

# 🚀 Phase 4 – Future-Proofing Features

# Once multi-user persistence works, you can expand:

# Feature	Description
# 🧠 AI Assistant	Integrate ChatGPT API to quiz or explain any subtopic.
# 📊 Global Dashboard	Leaderboard or completion summary across users.
# 📚 Resource Manager	Central JSON that defines all topics/subtopics for all domains.
# 💾 Cloud DB	Swap SQLite → PostgreSQL (Supabase or Railway) for web hosting.
# 🔄 Versioning	Store “study sessions” history over time, show trends.
# 🔍 Smart Search	Global search across topics, notes, and resources.
# 📆 Scheduler	Create reminders to review a topic every few days.
# 🧱 Learning Templates	Copy this entire system for AI, ML, DevOps, etc.
# 🧭 Summary
# Phase	Goal	Output
# 1️⃣	Multi-page modular layout	/pages/ per learning path
# 2️⃣	Persistent local DB	SQLite backend
# 3️⃣	Multi-user login	Secure session per user
# 4️⃣	AI & Analytics	Recommendation engine, quiz, timeline

# If you’d like, I can generate a ready-to-run starter package (zip) containing:

# Home.py

# pages/1_Oracle_Study.py

# utils/db.py

# Example SQLite schema

# A few placeholder assets

# Would you like me to build that next?
# You’d just unzip → run streamlit run Home.py → and have your multi-page study site live.

import streamlit as st
import json
from datetime import datetime
from urllib.parse import quote_plus
import pandas as pd
# -------------------------
# Note: Page config is handled by the main app
# -------------------------
# Helper data & functions
# -------------------------
TOPICS = {
    "A. Oracle Core Architecture (Foundation)": [
        {"id": "db_structure", "title": "Oracle Database Structure", "desc": "SGA, PGA, and background processes (SMON, PMON, DBWR, LGWR)."
        "System Global Area (SGA): This is a shared memory region accessible by all server and background processes of an Oracle instance. It contains data and control information for the instance. Key components of the SGA include: Shared Pool:  Database Buffer Cache: Redo Log Buffer"
        "Program Global Area (PGA): This is a private memory region allocated for each server process when it connects to the database. It is not shared with other processes. The PGA contains session-specific information and data for SQL execution.   Key components include: Sort Area: Hash Area: Private SQL Area"
        "Background Processes:"
        "SMON (System Monitor): Performs instance recovery in case of a crash, cleans up temporary segments, and coalesces free extents in tablespaces. It also performs other housekeeping tasks."
        "PMON (Process Monitor): Cleans up failed user processes by releasing resources, rolling back uncommitted transactions, and releasing locks."
        "DBWR (Database Writer): Writes modified data blocks (dirty buffers) from the Database Buffer Cache in the SGA to the database datafiles on disk."
        "LGWR (Log Writer): Writes redo log entries from the Redo Log Buffer in the SGA to the online redo log files on disk. This process is crucial for database recovery.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/",
                       "Oracle Base": "https://oracle-base.com/articles/misc/regular-expressions-support-in-oracle",
                       "LiveSQL": "https://livesql.oracle.com/",
                       "YouTube": "https://www.youtube.com/results?search_query=Oracle+SGA+PGA+background+processes"}},
        {"id": "storage_layers", "title": "Tablespaces, Datafiles, Redo & Undo", "desc": "Tablespaces, control files, datafiles, redo logs, undo/redo internals.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/12c/tablespaces"}},
        {"id": "startup_params", "title": "Startup & Parameter Files", "desc": "Startup/shutdown stages, parameter files (SPFILE/PFILE).",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/12c/oracle-startup-and-shutdown"}},
        {"id": "memory_tuning", "title": "PGA/SGA Tuning", "desc": "Memory management concepts and tuning strategies.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/11g/automatic-memory-management"}},
        {"id": "awr_latches", "title": "Wait Events, Latches & AWR", "desc": "Understanding waits, latches, and reading AWR reports.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/performance/awr-basics"}}
    ],

    "B. SQL Mastery for PL/SQL Developers": [
        {"id": "ddl_dml_tcl", "title": "SQL Command Families", "desc": "DDL, DML, DCL, and TCL command sets.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}},
        {"id": "joins_subqueries", "title": "Joins & Subqueries", "desc": "Inner/outer/self/cross joins, correlated subqueries.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/joins"}},
        {"id": "analytics", "title": "GROUP BY & Analytic Functions", "desc": "GROUP BY, HAVING, RANK, LAG, LEAD, DENSE_RANK usage.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/analytic-functions"}},
        {"id": "hierarchical", "title": "Hierarchical Queries", "desc": "CONNECT BY and START WITH constructs.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/hierarchical-queries"}},
        {"id": "set_ops_cte", "title": "Set Operators & CTEs", "desc": "UNION, INTERSECT, MINUS, WITH clause (CTEs).",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}}
    ],

    "C. PL/SQL Core Fundamentals": [
        {"id": "block_vars", "title": "Block Structure & Variables", "desc": "PL/SQL block structure, variables, datatypes, scopes.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/plsql-block-structure"}},
        {"id": "cursors", "title": "Cursors", "desc": "Implicit/explicit cursors, attributes (%FOUND, %NOTFOUND, etc.), parameterized cursors.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/cursor-handling"}},
        {"id": "control_flow", "title": "Control Structures", "desc": "IF, CASE, and looping constructs.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}},
        {"id": "exceptions", "title": "Exception Handling", "desc": "Predefined vs user-defined, propagation, logging.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/exception-handling"}},
        {"id": "parameters", "title": "Parameter Modes & Subprograms", "desc": "IN/OUT/IN OUT modes, procedure vs function differences.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}}
    ],

    "D. Modularization and Reusability": [
        {"id": "packages", "title": "Packages", "desc": "Specification/body, benefits, initialization sections.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/plsql-packages"}},
        {"id": "triggers", "title": "Triggers", "desc": "Statement vs row-level triggers, compound triggers, mutating table avoidance.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/triggers"}},
        {"id": "overloading", "title": "Overloading & Dependencies", "desc": "Handling overloaded procedures and dependency tracking.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}},
        {"id": "versioning", "title": "Version Control & CI/CD", "desc": "Using Git, Jenkins for DB code deployment.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/git-version-control"}}
    ],

    "E. Collections, Records, and Bulk Processing": [
        {"id": "records_rowtype", "title": "Records & %ROWTYPE", "desc": "RECORD types, rowtype-based records.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}},
        {"id": "collections", "title": "Collections", "desc": "Associative arrays, nested tables, VARRAYs.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/plsql-collections"}},
        {"id": "bulk_ops", "title": "Bulk Processing", "desc": "BULK COLLECT, FORALL, SAVE EXCEPTIONS patterns.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/bulk-collect-forall"}},
        {"id": "bulk_errors", "title": "Bulk DML Error Handling", "desc": "Handling errors during bulk operations.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}}
    ],

    "F. Advanced PL/SQL Programming": [
        {"id": "dynamic_sql", "title": "Dynamic SQL", "desc": "EXECUTE IMMEDIATE, DBMS_SQL usage.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/dynamic-sql"}},
        {"id": "ref_cursors", "title": "REF CURSORS", "desc": "Cursor variables and result-set management.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}},
        {"id": "autonomous_txn", "title": "Autonomous Transactions", "desc": "Logging & audit use cases.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/autonomous-transactions"}},
        {"id": "result_cache", "title": "Result Cache & Pipelined Functions", "desc": "Performance-oriented design features.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/function-result-cache"}},
        {"id": "compile_optimize", "title": "Conditional Compilation & Profiling", "desc": "Using $IF, optimization levels, DBMS_PROFILER.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}}
    ],

    "G. Performance Tuning & Optimization": [
        {"id": "explain_plan", "title": "EXPLAIN PLAN & AWR", "desc": "EXPLAIN PLAN, AUTOTRACE, TKPROF, AWR reports.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/performance/awr-basics"}},
        {"id": "optimizer", "title": "Optimizer Concepts", "desc": "CBO, bind variables, adaptive plans.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/query-optimizer"}},
        {"id": "indexing", "title": "Indexing Strategies", "desc": "B-tree, bitmap, function-based indexes.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/indexes"}},
        {"id": "stats_mviews", "title": "Statistics & Materialized Views", "desc": "Gathering stats and query rewrite.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}}
    ],

    "H. Transactions, Concurrency, and Locking": [
        {"id": "commit_rollback", "title": "Transaction Control", "desc": "COMMIT, ROLLBACK, SAVEPOINT.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}},
        {"id": "locking", "title": "Locking & Isolation Levels", "desc": "Row/table locks, deadlocks, isolation levels.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/locking"}},
        {"id": "auton_txn", "title": "Autonomous Transactions", "desc": "Using autonomous blocks for auditing/logging.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/autonomous-transactions"}},
        {"id": "redo_undo", "title": "Redo/Undo Internals", "desc": "Understanding redo, undo segments, rollback.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}}
    ],

    "I. Database Security and Auditing": [
        {"id": "roles_privs", "title": "Roles & Privileges", "desc": "User management, grants, schema ownership models.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/roles-and-privileges"}},
        {"id": "auditing", "title": "Unified & Fine-Grained Auditing", "desc": "Using FGA and unified audit trail.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/auditing"}},
        {"id": "vpd", "title": "Virtual Private Database", "desc": "Row-level security concepts.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/vpd"}},
        {"id": "sql_injection", "title": "SQL Injection Prevention", "desc": "Secure coding and definer/invoker rights.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}}
    ],

    "J. Job Scheduling and Automation": [
        {"id": "scheduler", "title": "DBMS_SCHEDULER", "desc": "Job chains, windows, classes.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/dbms_scheduler"}},
        {"id": "events", "title": "Event & File-based Jobs", "desc": "File arrival triggers and event-based scheduling.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}},
        {"id": "monitor_jobs", "title": "Monitoring & Troubleshooting Jobs", "desc": "Tracking job runs and logs.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/dbms_scheduler"}}
    ],

    "K. Data Migration and Integration": [
        {"id": "datapump", "title": "Data Pump & Transportable Tablespaces", "desc": "Export/import utilities, schema migration.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/12c/data-pump-12c"}},
        {"id": "zdm_gg", "title": "Zero Downtime & GoldenGate", "desc": "ZDM, GoldenGate real-time replication concepts.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/middleware/goldengate/"}},
        {"id": "etl_scripts", "title": "ETL & Automation", "desc": "Shell/Python scripting for migration.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/shell-scripting"}},
        {"id": "external_loader", "title": "External Tables & SQL*Loader", "desc": "Data loading techniques.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/12c/external-tables-12cr1"}}
    ],

    "L. PL/SQL in Modern Architectures": [
        {"id": "ords", "title": "ORDS REST APIs", "desc": "Expose PL/SQL via ORDS.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/oracle-rest-data-services"}},
        {"id": "json", "title": "JSON Handling", "desc": "JSON_OBJECT_T, JSON_TABLE examples.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/12c/json-support-in-oracle-database-12cr1"}},
        {"id": "external_procs", "title": "External Procedures", "desc": "Calling Java/C from PL/SQL.",
         "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}},
        {"id": "securefiles", "title": "SecureFile LOBs", "desc": "Working with large object storage efficiently.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/11g/securefiles"}},
        {"id": "ci_cd", "title": "CI/CD & Docker", "desc": "Integrating Oracle XE containers and pipelines.",
         "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/docker"}}
    ]
}


# TOPICS = {
#     "A. Oracle Core Architecture (Foundation)": [
#         {
#             "id": "sga_pga",
#             "title": "SGA, PGA & Background Processes",
#             "desc": "SGA, PGA, and important background processes (SMON, PMON, DBWR, LGWR).",
#             "resources": {
#                 "Oracle Docs": "https://docs.oracle.com/en/database/",
#                 "Oracle Base": "https://oracle-base.com/articles/11g/elementary-oracle-database-architecture",
#                 "LiveSQL Examples": "https://livesql.oracle.com/",
#                 "YouTube Search": "https://www.youtube.com/results?search_query=" + quote_plus("Oracle SGA PGA SMON PMON LGWR")
#             }
#         },
#         {
#             "id": "files_logs",
#             "title": "Tablespaces, Datafiles & Redo Logs",
#             "desc": "Tablespaces, datafiles, control files, redo logs and undo internals.",
#             "resources": {
#                 "Oracle Docs": "https://docs.oracle.com/en/database/",
#                 "Oracle Base": "https://oracle-base.com/articles/12c/tablespaces",
#                 "YouTube Search": "https://www.youtube.com/results?search_query=" + quote_plus("Oracle tablespaces redo logs datafiles")
#             }
#         },
#         {
#             "id": "startup_params",
#             "title": "Startup / Shutdown & Init Parameters",
#             "desc": "Database startup/shutdown phases and init/SPFILE parameters.",
#             "resources": {
#                 "Oracle Docs": "https://docs.oracle.com/en/database/",
#                 "Oracle Base": "https://oracle-base.com/articles/12c/oracle-startup-and-shutdown",
#                 "YouTube Search": "https://www.youtube.com/results?search_query=" + quote_plus("Oracle startup shutdown SPFILE PFILE")
#             }
#         }
#     ],

#     "B. SQL Mastery for PL/SQL Developers": [
#         {
#             "id": "joins_analytics",
#             "title": "Joins, Subqueries & Analytical Functions",
#             "desc": "Inner/outer joins, correlated subqueries, GROUP BY, HAVING, RANK, DENSE_RANK, LEAD, LAG.",
#             "resources": {
#                 "Oracle Base": "https://oracle-base.com/articles/misc/analytical-functions",
#                 "LiveSQL": "https://livesql.oracle.com/",
#                 "YouTube": "https://www.youtube.com/results?search_query=" + quote_plus("Oracle SQL joins subqueries analytic functions")
#             }
#         },
#         {
#             "id": "hierarchical_queries",
#             "title": "Hierarchical Queries & Set Operations",
#             "desc": "Using CONNECT BY, START WITH, UNION, INTERSECT, MINUS operations.",
#             "resources": {
#                 "Oracle Base": "https://oracle-base.com/articles/misc/hierarchical-queries",
#                 "LiveSQL": "https://livesql.oracle.com/",
#                 "YouTube": "https://www.youtube.com/results?search_query=" + quote_plus("Oracle hierarchical query connect by start with")
#             }
#         }
#     ],

#     "C. PL/SQL Core Fundamentals": [
#         {
#             "id": "block_structure",
#             "title": "PL/SQL Block Structure & Variables",
#             "desc": "Learn DECLARE, BEGIN, EXCEPTION sections and variable scope.",
#             "resources": {
#                 "Oracle Base": "https://oracle-base.com/articles/misc/plsql-block-structure",
#                 "LiveSQL": "https://livesql.oracle.com/",
#                 "YouTube": "https://www.youtube.com/results?search_query=" + quote_plus("Oracle PL/SQL block structure variables")
#             }
#         },
#         {
#             "id": "cursors_exceptions",
#             "title": "Cursors & Exception Handling",
#             "desc": "Explicit vs implicit cursors, user-defined exceptions, and propagation.",
#             "resources": {
#                 "Oracle Base": "https://oracle-base.com/articles/misc/exception-handling",
#                 "YouTube": "https://www.youtube.com/results?search_query=" + quote_plus("Oracle PL/SQL cursor exception handling")
#             }
#         }
#     ],

#     "D. Modularization and Reusability": [
#         {"id": "packages", "title": "Packages", "desc": "Specification vs body, modular programming, initialization sections.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/plsql-packages"}},
#         {"id": "triggers", "title": "Triggers", "desc": "Statement vs row-level triggers, compound triggers.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/triggers"}}
#     ],

#     "E. Collections and Bulk Processing": [
#         {"id": "collections", "title": "Collections & Records", "desc": "Associative arrays, nested tables, VARRAYs.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/plsql-collections"}},
#         {"id": "bulk_ops", "title": "Bulk Operations", "desc": "BULK COLLECT, FORALL, SAVE EXCEPTIONS patterns.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/bulk-collect-forall"}}
#     ],

#     "F. Advanced PL/SQL Programming": [
#         {"id": "dynamic_sql", "title": "Dynamic SQL & Ref Cursors", "desc": "EXECUTE IMMEDIATE, DBMS_SQL, cursor variables.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/dynamic-sql"}},
#         {"id": "autonomous_txn", "title": "Autonomous Transactions & Result Cache", "desc": "Logging, caching and advanced design.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/autonomous-transactions"}}
#     ],

#     "G. Performance Tuning and Optimization": [
#         {"id": "explain_plan", "title": "EXPLAIN PLAN & AWR", "desc": "Query tuning using EXPLAIN PLAN, TKPROF, and AWR.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/performance/awr-basics"}},
#         {"id": "optimizer_indexing", "title": "Optimizer & Indexing Strategies", "desc": "CBO, bind variables, B-tree vs bitmap indexes.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/query-optimizer"}}
#     ],

#     "H. Transactions and Concurrency": [
#         {"id": "txn_control", "title": "Transaction Control", "desc": "COMMIT, ROLLBACK, SAVEPOINT handling.",
#          "resources": {"Oracle Docs": "https://docs.oracle.com/en/database/"}},
#         {"id": "locking", "title": "Locking & Isolation", "desc": "Row-level, table-level locks, deadlocks, and isolation levels.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/locking"}}
#     ],

#     "I. Database Security and Auditing": [
#         {"id": "privileges", "title": "Privileges, Roles & Users", "desc": "User management and roles.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/roles-and-privileges"}},
#         {"id": "auditing", "title": "Auditing & SQL Injection Prevention", "desc": "Unified and fine-grained auditing, security best practices.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/auditing"}}
#     ],

#     "J. Job Scheduling and Automation": [
#         {"id": "scheduler", "title": "DBMS_SCHEDULER Basics", "desc": "Create and manage jobs, job chains, windows.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/dbms_scheduler"}},
#         {"id": "event_jobs", "title": "Event & File-based Scheduling", "desc": "Triggers, monitoring and job classes.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/dbms_scheduler"}}
#     ],

#     "K. Data Migration and Integration": [
#         {"id": "datapump", "title": "Data Pump & Transportable Tablespaces", "desc": "Export/import utilities and schema moves.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/12c/data-pump-12c"}},
#         {"id": "goldengate", "title": "GoldenGate & Zero Downtime Migration", "desc": "Real-time replication and migration tools.",
#          "resources": {"Oracle Docs": "https://docs.oracle.com/en/middleware/goldengate/" }}
#     ],

#     "L. PL/SQL in Modern Architectures": [
#         {"id": "ords", "title": "ORDS & REST APIs", "desc": "Expose PL/SQL as RESTful services.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/misc/oracle-rest-data-services"}},
#         {"id": "json", "title": "JSON & External Integrations", "desc": "Working with JSON_TABLE, external C/Java calls.",
#          "resources": {"Oracle Base": "https://oracle-base.com/articles/12c/json-support-in-oracle-database-12cr1"}}
#     ]
# }

PROGRESS_FILENAME = "oracle_progress.json"
LOG_FILENAME = "study_log.json"

# def init_state(subtopics):
#     if "progress" not in st.session_state:
#         st.session_state.progress = {s["id"]: "not started" for s in subtopics}
#     if "notes" not in st.session_state:
#         st.session_state.notes = {s["id"]: "" for s in subtopics}
#     if "log" not in st.session_state:
#         st.session_state.log = []
#     if "selected" not in st.session_state:
#         st.session_state.selected = subtopics[0]["id"]

def init_state(subtopics, topic_key):
    """
    Initialize session state safely per topic. Ensures we always have matching keys.
    """
    # Create per-topic identifiers to isolate progress between topics
    progress_key = f"progress_{topic_key}"
    notes_key = f"notes_{topic_key}"

    if progress_key not in st.session_state:
        st.session_state[progress_key] = {s["id"]: "not started" for s in subtopics}
    if notes_key not in st.session_state:
        st.session_state[notes_key] = {s["id"]: "" for s in subtopics}

    # Set active pointers to the currently selected topic's dicts
    st.session_state.progress = st.session_state[progress_key]
    st.session_state.notes = st.session_state[notes_key]

    if "log" not in st.session_state:
        st.session_state.log = []
    if "selected" not in st.session_state or st.session_state.selected not in [s["id"] for s in subtopics]:
        st.session_state.selected = subtopics[0]["id"]


def set_selected(sid):
    st.session_state.selected = sid

def export_progress():
    payload = {
        "progress": st.session_state.progress,
        "notes": st.session_state.notes,
        "log": st.session_state.log,
        "exported_at": datetime.utcnow().isoformat() + "Z"
    }
    return json.dumps(payload, indent=2)

def import_progress(json_str):
    try:
        data = json.loads(json_str)
        if "progress" in data and "notes" in data:
            st.session_state.progress.update(data["progress"])
            st.session_state.notes.update(data["notes"])
            if "log" in data:
                st.session_state.log = data["log"]
            st.success("Progress imported.")
        else:
            st.error("Invalid JSON structure. Need 'progress' and 'notes' keys.")
    except Exception as e:
        st.error(f"Failed to import: {e}")

def compute_summary():
    summary = []
    total_subtopics = 0
    total_done = 0

    for topic, subs in TOPICS.items():
        progress_key = f"progress_{topic}"
        if progress_key in st.session_state:
            prog = st.session_state[progress_key]
        else:
            prog = {s["id"]: "not started" for s in subs}

        done = sum(1 for v in prog.values() if v == "done")
        inprog = sum(1 for v in prog.values() if v == "in progress")
        total = len(subs)

        total_subtopics += total
        total_done += done

        summary.append({
            "Topic": topic,
            "Completed": done,
            "In Progress": inprog,
            "Total": total,
            "Completion %": round((done / total) * 100, 1)
        })

    overall = round((total_done / total_subtopics) * 100, 1)
    return summary, overall


# -------------------------
# UI layout
# -------------------------
st.sidebar.markdown("### 📊 Dashboard Views")
view_mode = st.sidebar.radio("Choose view:", ["Study Dashboard", "Progress Summary"])

if view_mode == "Progress Summary":
    st.title("📈 Overall Study Progress Summary")

    summary, overall = compute_summary()
    st.metric("Overall Completion", f"{overall}%")

    df = pd.DataFrame(summary)
    st.dataframe(df, width='stretch')

    st.bar_chart(df.set_index("Topic")["Completion %"])

    st.stop()


st.sidebar.title("Study Dashboard")
topic_names = list(TOPICS.keys())
selected_topic = st.sidebar.selectbox("Select Study Area", topic_names)
SUBTOPICS = TOPICS[selected_topic]
# init_state(SUBTOPICS)
init_state(SUBTOPICS, selected_topic)


progress_count = sum(1 for v in st.session_state.progress.values() if v == "done")
total = len(SUBTOPICS)
st.sidebar.progress(int((progress_count / total) * 100))
st.sidebar.caption(f"{progress_count}/{total} subtopics complete")

st.sidebar.markdown("---")
st.sidebar.markdown("**Jump to topic**")
for s in SUBTOPICS:
    if st.sidebar.button(s["title"], key=f"jump_{s['id']}"):
        set_selected(s["id"])

st.sidebar.markdown("---")
if st.sidebar.button("Reset Progress"):
    for k in st.session_state.progress.keys():
        st.session_state.progress[k] = "not started"
    st.success("Progress reset.")
st.sidebar.download_button("Export JSON", data=export_progress(), file_name=PROGRESS_FILENAME)
uploaded = st.sidebar.file_uploader("Import Progress JSON", type=["json"])
if uploaded:
    import_progress(uploaded.getvalue().decode("utf-8"))

# -------------------------
# Main content
# -------------------------
st.title("Oracle PL/SQL — Study Launcher")
st.subheader(selected_topic)

left_col, right_col = st.columns([1, 2])

with left_col:
    st.markdown("### Subtopics")
    for s in SUBTOPICS:
        cols = st.columns([0.7, 0.3])
        with cols[0]:
            if st.button(s["title"], key=f"list_{s['id']}"):
                set_selected(s["id"])
        with cols[1]:
            status = st.session_state.progress[s["id"]]
            if status == "done":
                st.success("Done")
            elif status == "in progress":
                st.info("In Progress")
            else:
                st.write("Not started")

with right_col:
    selected = next(filter(lambda x: x["id"] == st.session_state.selected, SUBTOPICS))
    st.markdown(f"## {selected['title']}")
    st.write(selected["desc"])

    st.markdown("#### Resources")
    for name, url in selected["resources"].items():
        st.markdown(f'- <a href="{url}" target="_blank">{name}</a>', unsafe_allow_html=True)

    st.markdown("#### Quick Actions")
    c1, c2, c3 = st.columns(3)
    if c1.button("Not Started"):
        st.session_state.progress[selected["id"]] = "not started"
    if c2.button("In Progress"):
        st.session_state.progress[selected["id"]] = "in progress"
    if c3.button("Done"):
        st.session_state.progress[selected["id"]] = "done"

    st.markdown("#### Notes")
    note = st.text_area("Add notes:", value=st.session_state.notes[selected["id"]], key=f"note_{selected['id']}")
    if st.button("Save Note"):
        st.session_state.notes[selected["id"]] = note
        st.success("Note saved.")

st.markdown("---")
st.caption("Made with ❤️ to streamline your Oracle PL/SQL prep.")
