# Glossary

Names a new reader meets on the first pages. One line each. The design is [Design](IMPLEMENTATION.md). How to quote a number is [Interpreting results](INTERPRETING_RESULTS.md).

| Name | Means |
|---|---|
| LEO | An attempt, in epilepsy, to turn specialty literature into research software: rules, a constrained clinical model, codes after extract, and a person on every clash. Transfer to another specialty is untested |
| Research extract | A cell that is `accepted` **and** both readers (`specialist+llm`). On the 40 letters, concordant PPV 71/82 = 0.866. Clashes are flagged for review |
| D17 | On a clash, show the rules; keep the model value as `alternative` |
| L1C | Med42-8B, flat prompt, two fixed examples, schema-constrained greedy decoding |
| E / EpExtra | The rules reader: MedCAT + ExECT-style field rules + medspaCy ConText |
| O | Ontology codes attached after the value exists. O does not vote and does not raise precision |
| F-S | The 40 held-out Fonferko-Shadrach letters (synthetic, clinician-authored) |
| `leo-v0.9` | Current pipeline tag |

The frozen evaluation log is `docs/EVAL_PROTOCOL_LEO.md` in the repo. It is not on the public site.
