"""The agent's one tool. Every failure comes back as text, so the model can fix it."""
import threading
from pathlib import Path

import duckdb

DB_PATH = Path(__file__).resolve().parent.parent / "sandbox" / "tpch.duckdb"
MAX_ROWS = 20
MAX_CHARS = 2000
QUERY_SECONDS = 10

# The model only ever sees this description. It never touches the database itself.
TOOLS = [{
    "type": "function",
    "function": {
        "name": "run_sql",
        "description": f"Run one read-only SELECT query. Returns at most {MAX_ROWS} rows.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
}]


def is_single_select(connection, query):
    statements = connection.extract_statements(query)
    return len(statements) == 1 and statements[0].type == duckdb.StatementType.SELECT


def run_sql(query):
    connection = duckdb.connect(
        str(DB_PATH),
        read_only=True,
        config={"enable_external_access": False},     # no reading files from this machine
    )
    timer = threading.Timer(QUERY_SECONDS, connection.interrupt)
    timer.start()
    try:
        if not is_single_select(connection, query):
            return "Rejected: send exactly one SELECT query."
        rows = connection.execute(query).fetchmany(MAX_ROWS + 1)
        text = str(rows[:MAX_ROWS])
        if len(rows) > MAX_ROWS:                      # never drop rows silently
            text += f"\nOnly the first {MAX_ROWS} rows are shown. More exist."
        if len(text) > MAX_CHARS:
            text = text[:MAX_CHARS] + "\nResult cut short: it was too long."
        return text
    except duckdb.Error as error:
        return f"SQL error: {error}"
    finally:
        timer.cancel()
        connection.close()
