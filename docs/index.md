# LEO

**Research phenotyping for epilepsy notes.**

Full documentation at [https://medai.readthedocs.io](https://medai.readthedocs.io).

> **Research use only.** Does not diagnose or recommend treatment. Tested on **synthetic notes only**. Real notes need IRB and approved compute.

## What LEO does

LEO (Language, EpExtra, Ontology) is an attempt, in epilepsy, to turn specialty literature into research software: a rules reader, a constrained clinical model, codes after extract, and a person on every clash. Whether that pattern can become a framework for another specialty is untested. It reads a clinic letter and fills a phenotype table: seizure and epilepsy type, medications and status, EEG and MRI cues, and related fields. Every cell carries a value, a quote from the note, which reader produced it, and whether a person should look. The aim is a table a study can defend — agreed cells kept, clashes flagged for review.

A letter often supports more than one reading of the same sentence (current versus prior, plan versus fact, the patient’s drug versus family history). LEO therefore runs two different readers: a constrained clinical language model (Med42-8B) and deterministic ExECT-style rules. Cells where they agree become the research extract. Cells where they clash go to a review queue; the rules value is shown and the model value is kept as an alternative. An ontology layer can attach published codes after extract. It does not vote, and it is not used to raise precision.

This has been tested on **synthetic** clinician-authored letters only. It does not diagnose or recommend treatment. Accepted cells still miss gold about one time in six or seven (concordant PPV 71/82 = 0.866 on the 40-letter set). CPU-only runs have one reader and are not a research extract. Why the three parts exist: [Theory and Science](THEORY.md). How to quote a number: [Interpreting results](INTERPRETING_RESULTS.md).

## In practice

1. **Two readers, one table.** Constrained Med42-8B plus ExECT-style rules (EpExtra). Agree → accept. Clash → review; the **rules** are shown (D17); the model value is kept as `alternative`.
2. **One note = one row.** Roll-up is optional and is not the extract. The research extract is `accepted` **and** both readers.
3. **A Validator, not a chat.** Accept / Correct / Deny / add missed values. `leo learn` scores routing later; it does not change the extract.

Code: [github.com/phindagijimana/LEO](https://github.com/phindagijimana/LEO).

## Documentation

Study the work in this order: [Theory and Science](THEORY.md), [Interpreting results](INTERPRETING_RESULTS.md), [Design](IMPLEMENTATION.md), [Weaknesses](WEAKNESSES.md), [Literature](LITERATURE.md). Names on those pages: [Glossary](GLOSSARY.md).

| Page | Use |
|---|---|
| [Theory and Science](THEORY.md) | Why L, E, and O — and why they are not voted |
| [Interpreting results](INTERPRETING_RESULTS.md) | How to quote numbers |
| [Design](IMPLEMENTATION.md) | Why each step exists |
| [Weaknesses](WEAKNESSES.md) | What is still wrong |
| [Literature](LITERATURE.md) | Papers LEO cites |
| [Glossary](GLOSSARY.md) | D17, L1C, F-S, research extract, `leo-v0.9` |
| [Installation](LEO_HOSTING.md) | Workstation, Slurm, weights, UMLS |
| [Container](LEO_CONTAINER.md) | Docker / Apptainer; mount weights and CDB |
| [PHI scan](LEO_PHI.md) | HIPAA-18 flags; not de-id; not extract |
| [Research-host deploy](LEO_RESEARCH_DEPLOY.md) | `--research`: local weights, offline, no cloud |
| [IS request](LEO_IS_REQUEST.md) | Text to send privacy / research IS |
| [Third-party licenses](LEO_THIRD_PARTY.md) | Med42 / UMLS / CDB — not in git |
| [Quick start](QUICKSTART.md) | `bin/leo check` and a first batch |
| [Usage](LEO_USER_GUIDE.md) | Commands, input/output, Validator |
| [Routing rules](LEO_ROUTING_RULES.md) | ACCEPT / REVIEW / REJECT |
| [Learning](ACTIVE_LEARNING_PLAN.md) | `leo learn` (does not change the extract) |

## What this site does not include

This is the only documentation site. The evaluation log is on this site: [Evaluation protocol](EVAL_PROTOCOL_LEO.md). Lab plans, outreach notes, superseded drafts, and duplicate command sheets stay in the `docs/` folder of the repository and are not published here. Paper drafts in `writing/` and `paper_doc/`, and the raw hold-out tables under `eval/results/`, stay in the repository too.
