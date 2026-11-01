# learn-agents

Learn how AI agents work by building them from scratch in plain Python, with no frameworks.
Companion code for the **AI Simply** videos. Everything runs on your own laptop, for free.

Start with [m01: The agent loop](m01_agent_loop/README.md): a working agent in under 90 lines.

## What's in each folder

| Folder | What it holds |
|---|---|
| `m01_agent_loop/` | The lesson: the agent (`agent.py`), its one tool, a safe SQL runner (`tools.py`), and `break_it.py`, which shows the step limit stopping a runaway model. |
| `common/` | Helpers every lesson shares: `llm.py` talks to the model, `trace.py` saves each run to `logs/` so you can check any answer, and `fake_llm.py` is a scripted model for testing. |
| `sandbox/` | The practice database. `build_sandbox.py` creates it on your laptop, about 30 MB of sample data. |
| `tests/` | Automatic checks for the agent and its safety limits. They use the scripted model, so they need no real model. |

## Set up

You need Python 3.11 or newer.

```bash
git clone https://github.com/AISimplyNxt/learn-agents.git
cd learn-agents
python -m venv .venv
```

Activate it with `.venv\Scripts\activate` on Windows, or `source .venv/bin/activate` on macOS and Linux. Then:

```bash
pip install -r requirements.txt
python sandbox/build_sandbox.py
```

## Try it without a model

The tests and `break_it.py` use a scripted fake model, so they need no model and no graphics card.

```bash
pytest -q
python m01_agent_loop/break_it.py
```

## Run it with a real model

Install [Ollama](https://ollama.com), then:

```bash
ollama pull qwen3:4b
```

Copy `.env.example` to `.env`, and ask a question:

```bash
python m01_agent_loop/agent.py "Which nation has the most customers?"
```

On a laptop with a 4 GB graphics card, a run takes a few minutes, most of it loading the model
and thinking. The address and model name live in `.env`, so you can point this at any
OpenAI-compatible server without changing the code.

## Licence

[MIT](LICENSE)
