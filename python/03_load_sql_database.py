from pathlib import Path
import sqlite3
import pandas as pd

# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data" / "fpa_budget_actual_validated.csv"
SCHEMA_FILE = ROOT / "sql" / "01_schema.sql"
DB_FILE = ROOT / "data" / "fpa.db"


# ============================================================
# CHECK REQUIRED FILES
# ============================================================

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Validated CSV not found: {DATA_FILE}\n"
        "Run 01_validate_financials.py first."
    )

if not SCHEMA_FILE.exists():
    raise FileNotFoundError(
        f"Schema file not found: {SCHEMA_FILE}"
    )


# ============================================================
# LOAD VALIDATED CSV
# ============================================================

df = pd.read_csv(
    DATA_FILE,
    parse_dates=["Month"]
)


required = {
    "Month",
    "Department",
    "Account",
    "Budget",
    "Actual"
}

missing = required - set(df.columns)

if missing:
    raise ValueError(
        f"Missing required columns: {sorted(missing)}"
    )


# ============================================================
# CREATE DATABASE
# ============================================================

conn = sqlite3.connect(DB_FILE)

# Enable foreign-key enforcement in SQLite
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()


# ============================================================
# IMPORT AND EXECUTE EXISTING 01_schema.sql
# ============================================================

schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")

cursor.executescript(schema_sql)


# ============================================================
# LOAD DEPARTMENT DIMENSION
# ============================================================

departments = (
    df["Department"]
    .dropna()
    .drop_duplicates()
    .sort_values()
    .reset_index(drop=True)
)

department_rows = [
    (i + 1, department)
    for i, department in enumerate(departments)
]

cursor.executemany(
    """
    INSERT INTO dim_department
        (department_id, department_name)
    VALUES (?, ?)
    """,
    department_rows
)


# ============================================================
# LOAD ACCOUNT DIMENSION
# ============================================================

opex_accounts = {
    "Payroll",
    "Software",
    "Travel",
    "Facilities",
    "Other OpEx"
}

accounts = (
    df["Account"]
    .dropna()
    .drop_duplicates()
    .sort_values()
    .reset_index(drop=True)
)

account_rows = []

for i, account in enumerate(accounts, start=1):

    if account in opex_accounts:
        account_group = "OpEx"

    elif account == "Revenue":
        account_group = "Revenue"

    elif account == "COGS":
        account_group = "COGS"

    else:
        account_group = "Other"

    account_rows.append(
        (i, account, account_group)
    )


cursor.executemany(
    """
    INSERT INTO dim_account
        (account_id, account_name, account_group)
    VALUES (?, ?, ?)
    """,
    account_rows
)


# ============================================================
# CREATE LOOKUP DICTIONARIES
# ============================================================

department_lookup = {
    department_name: department_id
    for department_id, department_name
    in department_rows
}

account_lookup = {
    account_name: account_id
    for account_id, account_name, account_group
    in account_rows
}


# ============================================================
# LOAD FACT TABLE
# ============================================================

fact_rows = []

for _, row in df.iterrows():

    department_id = department_lookup[row["Department"]]

    account_id = account_lookup[row["Account"]]

    month = pd.to_datetime(row["Month"]).strftime("%Y-%m-%d")

    budget = float(row["Budget"])

    actual = float(row["Actual"])

    fact_rows.append(
        (
            month,
            department_id,
            account_id,
            budget,
            actual
        )
    )


cursor.executemany(
    """
    INSERT INTO fact_financials
        (
            month,
            department_id,
            account_id,
            budget,
            actual
        )
    VALUES (?, ?, ?, ?, ?)
    """,
    fact_rows
)


# ============================================================
# COMMIT
# ============================================================

conn.commit()


# ============================================================
# VALIDATION / RECONCILIATION
# ============================================================

department_count = cursor.execute(
    "SELECT COUNT(*) FROM dim_department"
).fetchone()[0]

account_count = cursor.execute(
    "SELECT COUNT(*) FROM dim_account"
).fetchone()[0]

fact_count = cursor.execute(
    "SELECT COUNT(*) FROM fact_financials"
).fetchone()[0]


csv_budget = df["Budget"].sum()

sql_budget = cursor.execute(
    "SELECT SUM(budget) FROM fact_financials"
).fetchone()[0]

csv_actual = df["Actual"].sum()

sql_actual = cursor.execute(
    "SELECT SUM(actual) FROM fact_financials"
).fetchone()[0]


# ============================================================
# RECONCILIATION CHECKS
# ============================================================

if fact_count != len(df):
    raise ValueError(
        f"Row-count mismatch: CSV={len(df)}, SQL={fact_count}"
    )

if abs(csv_budget - sql_budget) > 0.01:
    raise ValueError(
        f"Budget mismatch: CSV={csv_budget}, SQL={sql_budget}"
    )

if abs(csv_actual - sql_actual) > 0.01:
    raise ValueError(
        f"Actual mismatch: CSV={csv_actual}, SQL={sql_actual}"
    )


# ============================================================
# CLOSE DATABASE
# ============================================================

conn.close()


# ============================================================
# FINAL OUTPUT
# ============================================================

print("=" * 60)
print("FP&A SQL DATABASE LOAD COMPLETE")
print("=" * 60)

print(f"Schema imported:   {SCHEMA_FILE}")
print(f"Database:          {DB_FILE}")
print(f"CSV rows loaded:   {len(df):,}")
print(f"Departments:       {department_count}")
print(f"Accounts:          {account_count}")
print(f"Fact rows:         {fact_count:,}")
print(f"Total Budget:      {csv_budget:,.2f}")
print(f"Total Actual:      {csv_actual:,.2f}")

print("=" * 60)
print("Schema:            01_schema.sql")
print("Reconciliation:    PASSED")
print("=" * 60)