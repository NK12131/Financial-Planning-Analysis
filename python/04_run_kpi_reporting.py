from pathlib import Path
import sqlite3
import pandas as pd

# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

DB_FILE = ROOT / "data" / "fpa.db"
SQL_FILE = ROOT / "sql" / "02_kpi_reporting.sql"


# ============================================================
# CHECK FILES
# ============================================================

if not DB_FILE.exists():
    raise FileNotFoundError(
        f"Database not found: {DB_FILE}\n"
        "Run 03_load_sql_database.py first."
    )

if not SQL_FILE.exists():
    raise FileNotFoundError(
        f"SQL file not found: {SQL_FILE}"
    )


# ============================================================
# CONNECT TO DATABASE
# ============================================================

conn = sqlite3.connect(DB_FILE)


# ============================================================
# READ SQL FILE
# ============================================================

sql_text = SQL_FILE.read_text(encoding="utf-8")


# ============================================================
# SPLIT THE THREE QUERIES
# ============================================================

queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]


# ============================================================
# RUN EACH QUERY
# ============================================================

for i, query in enumerate(queries, start=1):

    print("\n" + "=" * 70)
    print(f"QUERY {i}")
    print("=" * 70)

    try:
        result = pd.read_sql_query(query, conn)

        if result.empty:
            print("Query executed successfully, but returned no rows.")

        else:
            print(result.to_string(index=False))

    except Exception as e:
        print(f"ERROR in Query {i}:")
        print(e)


# ============================================================
# CLOSE DATABASE
# ============================================================

conn.close()

print("\n" + "=" * 70)
print("SQL KPI REPORTING COMPLETE")
print("=" * 70)