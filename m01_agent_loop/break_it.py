"""Break it: a model that never stops asking. The step budget is all that saves us."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.fake_llm import FakeLLM, tool_call  # noqa: E402
from m01_agent_loop.agent import run_agent  # noqa: E402

stuck = FakeLLM([tool_call("run_sql", query="SELECT 1")] * 100)
print(run_agent("Loop forever, please.", llm=stuck, max_steps=3).answer)
print(f"The model was asked {len(stuck.seen)} times, not 100.")
