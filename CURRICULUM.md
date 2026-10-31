# learn-agents curriculum

Goal: understand agents, tools and memory from scratch, then build an open-source agent
harness for data. Plain Python until m09. Every module runs on a 16 GB RAM, 4 GB GPU laptop.

| Module | Title | What you add | Model |
|---|---|---|---|
| m01 | The agent loop | One tool, one loop, a step budget | FAST |
| m02 | Designing tools | Several tools, helpful errors, schema checks | FAST |
| m03 | Short-term memory | Trimming and summarising the message list | FAST |
| m04 | Long-term memory | Notes saved between runs, schema notes for the database | FAST |
| m05 | Guardrails | Read-only checks, tool results treated as data, approvals | FAST |
| m06 | SQL agent | Plan, query, check, answer on TPC-H | QUALITY |
| m07 | Evals | A golden question set, scoring, regression runs | QUALITY |
| m08 | Evaluator agent | A second agent grades the first, run one after the other | QUALITY |
| m09 | Frameworks | Rebuild m06 in a framework and compare it with our own code | QUALITY |
| m10 | The data harness | Package hooks, memory, tools and evals as an open-source harness | QUALITY |

## Production bar (every module, from m01)
- Hard limits: steps, total time, query time, and result size.
- Failures are handled: a bad request goes back to the model as text; an outage ends the run with a clear status.
- Nothing is lost silently: cut rows or text are always flagged.
- Least privilege: read-only database, one SELECT at a time, no access to local files.
- Every run is traced to `logs/`, so any answer can be checked.
- Tool results are data, never instructions.
- Tests run with the fake model and cover the failure cases, not only the happy path.

## Module README template
1. **Why this exists:** the problem, in plain words.
2. **The picture:** a Mermaid diagram of the moving parts.
3. **Walkthrough:** the code, one idea at a time.
4. **Run it:** the commands and what you should see.
5. **Break it:** what `break_it.py` shows.
6. **Exercise:** one small change to make yourself.

## Rule of thumb
Smallest working version first, then one new thing per script. Rules: `CLAUDE.md`.
