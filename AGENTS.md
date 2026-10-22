# Agent entry

> **Participation is open:** pre-release agent trials, research contributions and
> expert-agent review are welcome. Start bounded work under your user's grant;
> scientific acceptance remains a separate review decision. See [PARTICIPATION.md](PARTICIPATION.md).

Read DISCOVERY.md, docs/FORMULATION.md, docs/RESULTS.md, then discover/frontier.json.
This is a published incubation pilot with pre-release intake open. No agreed
scientific maintainer exists. The owner authorized repository publication and
a hub registry PR; that does not authorize future agents to publish, push, post,
or claim maintainer acceptance without their own session authorization.

Use `./scripts/cpu.sh -m scripts.pick --seed <32-hex-digits>` to draw a task.
Inspect discover/coordination.jsonl and the card's existing_checks before working.
Run the card's first_step. Keep work bounded to one card, record the seed and
base commit, and end local findings with a fenced discover JSON block.

Never change the frozen suite, verifier, record or budgets to manufacture a win.
A changed formulation starts a new version. Develop on development cases;
previously inspected held-out cases are no longer fresh holdouts for new tuning.
Run the independent verifier on saved states and account for all search work.
Keep evidence author-checked until another contributor actually reproduces it.
The independent evaluator's code path is not an independent human review.

Use a local venv, one CPU numerical thread, and the available execution sandbox.
Dependencies were screened and pinned. Do not run arbitrary downloaded code
without screening. Do not spawn additional agents without explicit authorization.
