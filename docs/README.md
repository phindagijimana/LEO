# Documentation

Study the work in this order:

1. [`THEORY.md`](THEORY.md) — why L, E, and O, and why they are not voted
2. [`INTERPRETING_RESULTS.md`](INTERPRETING_RESULTS.md) — which numbers can be quoted
3. [`IMPLEMENTATION.md`](IMPLEMENTATION.md) — design, decisions, where the code is
4. [`WEAKNESSES.md`](WEAKNESSES.md) — each hole, what accounts for it, what is next
5. [`LITERATURE.md`](LITERATURE.md) — papers these pages cite

Names on those pages: [`GLOSSARY.md`](GLOSSARY.md).

The judgment is in those pages, not in a separate biography. [`IMPLEMENTATION.md`](IMPLEMENTATION.md) records each design choice and the code that implements it. [`INTERPRETING_RESULTS.md`](INTERPRETING_RESULTS.md) records which numbers can be quoted. [`WEAKNESSES.md`](WEAKNESSES.md) records what was measured and left open. The deviation log is `EVAL_PROTOCOL_LEO.md` on disk. It is not published. The repository does not split that record by person.

## Operator pages

These are also the Read the Docs site (`docs_site/` is symlinks into this folder). Preview: `pip install -r docs_site/requirements.txt && mkdocs serve`.

| File | Use |
|---|---|
| [`index.md`](index.md) | Public landing |
| [`QUICKSTART.md`](QUICKSTART.md) | `bin/leo check` and a first batch |
| [`LEO_USER_GUIDE.md`](LEO_USER_GUIDE.md) | Commands, Validator, learn |
| [`LEO_HOSTING.md`](LEO_HOSTING.md) | Workstation, Slurm, weights |
| [`LEO_CONTAINER.md`](LEO_CONTAINER.md) | Docker / Apptainer |
| [`LEO_RESEARCH_DEPLOY.md`](LEO_RESEARCH_DEPLOY.md) | `--research`: local weights, offline, no cloud |
| [`LEO_PHI.md`](LEO_PHI.md) | HIPAA-18 flags; not de-identification |
| [`LEO_IS_REQUEST.md`](LEO_IS_REQUEST.md) | Text to send privacy / research IS |
| [`LEO_THIRD_PARTY.md`](LEO_THIRD_PARTY.md) | Med42, UMLS, CDB — not in git |
| [`LEO_ROUTING_RULES.md`](LEO_ROUTING_RULES.md) | ACCEPT / REVIEW / REJECT |
| [`ACTIVE_LEARNING_PLAN.md`](ACTIVE_LEARNING_PLAN.md) | `leo learn`; extract unchanged |

These files only point at the LEO guides above: `QUICK_START.md`, `HPC_CLI_GUIDE.md`, `RESOURCE_MODES.md`. At the repo root, `COMMANDS.md`, `PROJECT_STRUCTURE.md`, `DEPLOYMENT.md`, `SELF_HOSTING.md`, `TEST_RESULTS_SUMMARY.md`, and `REAL_WORLD_TEST_RESULTS.md` do the same.

## On this site

There is one documentation site, [medai.readthedocs.io](https://medai.readthedocs.io). The pages above are that site. Two short decision notes are there too: [`LORA_FLAT_CONTRACT.md`](LORA_FLAT_CONTRACT.md) and [`MEASURED_FAILURE_TECHNIQUES.md`](MEASURED_FAILURE_TECHNIQUES.md).

Everything else in this folder stays on disk. It is not on the site and not on GitHub. That includes the evaluation log, the long bibliography, the schema, scope notes, corpus plans, outreach, and superseded drafts.

Paper drafts in `writing/` and `paper_doc/` stay on disk. Hold-out tables under `eval/results/` stay in the repository.
