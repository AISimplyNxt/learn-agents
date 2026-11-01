import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.fake_llm import FakeLLM, answer, tool_call
from common.llm import LLMError
from common.trace import Trace
from m01_agent_loop import tools
from m01_agent_loop.agent import run_agent
from m01_agent_loop.tools import run_sql


@pytest.fixture
def trace(tmp_path):
    return Trace(tmp_path)


def test_answers_without_a_tool(trace):
    result = run_agent("Hi", llm=FakeLLM([answer("Hello")]), trace=trace)
    assert (result.status, result.answer, result.steps) == ("answered", "Hello", 1)


def test_tool_result_goes_back_to_the_model(trace):
    fake = FakeLLM([tool_call("run_sql", query="SELECT count(*) FROM orders"), answer("Done")])
    assert run_agent("How many orders?", llm=fake, trace=trace).answer == "Done"
    assert fake.seen[1][-1]["role"] == "tool"
    assert "150000" in fake.seen[1][-1]["content"]


def test_step_budget_stops_a_stuck_model(trace):
    fake = FakeLLM([tool_call("run_sql", query="SELECT 1")] * 10)
    result = run_agent("Go", llm=fake, max_steps=3, trace=trace)
    assert result.status == "step_limit"
    assert len(fake.seen) == 3


def test_time_limit_stops_the_run(trace):
    result = run_agent("Go", llm=FakeLLM([answer("Late")]), time_limit=-1, trace=trace)
    assert result.status == "time_limit"


def test_model_failure_is_reported_not_raised(trace):
    def down(messages, tools=None, model=None):
        raise LLMError("connection refused")
    result = run_agent("Go", llm=down, trace=trace)
    assert result.status == "model_error"
    assert "connection refused" in result.answer


def test_malformed_arguments_go_back_to_the_model(trace):
    bad = tool_call("run_sql", query="x")
    bad["tool_calls"][0]["function"]["arguments"] = "{not json"
    fake = FakeLLM([bad, answer("Done")])
    assert run_agent("Go", llm=fake, trace=trace).status == "answered"
    assert fake.seen[1][-1]["content"].startswith("Bad arguments")


def test_unknown_tool_goes_back_to_the_model(trace):
    fake = FakeLLM([tool_call("drop_database"), answer("Done")])
    assert run_agent("Go", llm=fake, trace=trace).status == "answered"
    assert fake.seen[1][-1]["content"].startswith("Unknown tool")


def test_every_run_is_traced(trace):
    fake = FakeLLM([tool_call("run_sql", query="SELECT 1"), answer("Done")])
    run_agent("Go", llm=fake, trace=trace)
    assert [line.count('"event"') for line in trace.path.read_text().splitlines()] == [1, 1, 1]


def test_sql_error_is_returned_not_raised():
    assert run_sql("SELECT nope FROM orders").startswith("SQL error")


@pytest.mark.parametrize("query", [
    "DELETE FROM orders",
    "DROP TABLE orders",
    "SELECT 1; SELECT 2",
    "COPY orders TO 'stolen.csv'",
])
def test_only_one_select_is_allowed(query):
    result = run_sql(query)
    assert result.startswith(("Rejected", "SQL error"))


def test_local_files_cannot_be_read():
    assert run_sql("SELECT * FROM read_text('README.md')").startswith("SQL error")


def test_extra_rows_are_flagged_not_dropped_silently():
    assert "More exist" in run_sql("SELECT * FROM range(21)")
    assert "More exist" not in run_sql("SELECT * FROM range(20)")


def test_long_results_are_cut_and_flagged(monkeypatch):
    monkeypatch.setattr(tools, "MAX_CHARS", 50)
    assert "cut short" in run_sql("SELECT * FROM orders")


def test_slow_query_is_stopped(monkeypatch):
    monkeypatch.setattr(tools, "QUERY_SECONDS", 0.2)
    assert run_sql("SELECT count(*) FROM range(100000000000) a, range(100000) b").startswith("SQL error")
