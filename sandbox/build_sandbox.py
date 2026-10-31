"""Build the practice database: TPC-H scale factor 0.1, about 30 MB. Run once.

    python sandbox/build_sandbox.py
"""
from pathlib import Path

import duckdb

DB_PATH = Path(__file__).resolve().parent / "tpch.duckdb"

if DB_PATH.exists():
    print(f"Already there: {DB_PATH}")
else:
    con = duckdb.connect(str(DB_PATH))
    con.execute("INSTALL tpch")                # DuckDB's own data generator, downloaded once
    con.execute("LOAD tpch")
    con.execute("CALL dbgen(sf=0.1)")
    con.close()
    print(f"Built {DB_PATH}")
