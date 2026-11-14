# Prompting and fine-tuning

How the language-model reader was chosen. Same 40 synthetic Fonferko-Shadrach letters, seven fields, micro-F1, letter bootstrap, seed 0. Each arm is a script and a saved manifest. A prompt or an adapter is shipped only when it fills fields and does not make the fused table worse. The day-by-day log stays on disk in `docs/EVAL_PROTOCOL_LEO.md`.

The model is Med42-8B [Christophe et al. 2024], an open clinical Llama 3 we can run on approved compute. Task-specific fine-tuning for epilepsy notes is a published path [Xie 2023; Decker 2022; Abeysinghe 2025]. Those checkpoints are not loaded. Chain-of-thought, a 70B model, and self-consistency are exam-style question answering. They are a different job from filling a phenotype cell. LoRA is the fine-tune method (Hugging Face PEFT). Reporting follows TRIPOD-LLM [Gallifant 2025]. Papers: [Literature](LITERATURE.md).

## Process

1. Write one arm: a prompt, or a prompt plus constrained decoding, or a LoRA adapter on that same flat contract.
2. Run it on the frozen 40 letters. Greedy, seed 0.
3. Score the model alone and the fused table (rules + model) against gold.
4. Keep the arm if the output is usable and fusion does not get worse. Otherwise record the negative and leave the shipped reader unchanged.

## Prompting

Early prompts pasted the JSON schema into the instruction (M0–M2). The model echoed the schema instead of filling fields. That is a reported negative (F3). The shipped prompt does not contain the schema. Decoding is constrained to the schema instead.

The prompt that remains is flat: the field list, two fixed examples, and the note. Zero-shot, two examples, and retrieved examples were all run, with and without the constraint.

| Arm | What changed | Model alone, micro-F1 | What it showed |
|---|---|---:|---|
| L0 | Flat prompt, no example | 0.679 | A plain clinical 8B already matches the rules on these seven fields |
| L1 | Two fixed examples | 0.700 | A small, stable gain over zero-shot |
| L2 | Three retrieved letters as examples | 0.678 | Retrieval did not help. Four letters had no usable output |
| L1C | L1, schema-constrained | 0.700 | Same accuracy as L1. Every letter usable. Quotes are verbatim |
| L2C | L2, schema-constrained | 0.736 | The constraint, not the extra examples, was the gain (L2C − L2 +0.059 [0.017, 0.110]) |

L2C is not clearly better than L1C (difference interval includes 0). The shipped reader is L1C: two examples, constrained, greedy, seed 0. It is the frozen contract the headline numbers use.

## Fine-tuning

The first adapter (arm H) was a LoRA on the same flat contract, trained to emit the gold table. On the 40 letters the model alone reached 0.752. That is not separable from the best constrained prompt (arm H − L2C +0.016 [−0.061, +0.098]). Of 177 field quotes, 24 were verbatim. The adapter copied training strings such as “levetiracetam 250.0 mg twice daily” that are not in the letter. Fusion was worse than the adapter alone (reviewed − model −0.089 [−0.157, −0.016]).

A later adapter on that contract (H2) is about +0.04 F1 versus L1C (0.74 versus 0.70) for the model alone. Fused, reviewed F1 is about 0.69, below the adapter alone. The adapter was trained to match gold, not to agree with the rules, so on a clash it fights the rules reader. H2 stays off fusion. `--h2` is opt-in. Detail: [LoRA contract](LORA_FLAT_CONTRACT.md).

What was tried and left unused:

- Training on the M2 schema-echo traces.
- Treating a MedQA LoRA score as a phenotyping gain.
- A live adapter from reviewer clicks. Loop C is paused until a frozen hold-out exists. `leo learn --lora` is refused.

If an adapter is trained again, the positive examples are cells where the rules and L1C already agree and the quote supports the cell, plus reviewer-corrected quotes after IRB. The loss stays the flat-contract JSON. The goal is an adapter that copies the rules where the rules are right and adds recall only where the rules were silent.
