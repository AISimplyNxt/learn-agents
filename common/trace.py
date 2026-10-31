"""Writes every run to logs/<run id>.jsonl, so any answer can be checked afterwards."""
import json
import time
import uuid
from pathlib import Path

LOGS = Path(__file__).resolve().parent.parent / "logs"


class Trace:
    def __init__(self, logs=LOGS):
        logs.mkdir(exist_ok=True)
        self.run_id = uuid.uuid4().hex[:12]
        self.path = logs / f"{self.run_id}.jsonl"

    def log(self, event, **fields):
        record = {"time": time.time(), "run": self.run_id, "event": event, **fields}
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, default=str) + "\n")
