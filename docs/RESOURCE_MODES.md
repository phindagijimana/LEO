# CPU and GPU

| Mode | Command | What you get |
|---|---|---|
| Rules only | `bin/leo batch notes.xlsx --cpu` or `--local --mode cpu` | One reader. Every cell `needs_review`. Not a research extract. |
| Both readers | `bin/leo batch notes.xlsx` (Slurm GPU) or `--local --mode gpu` | Med42-8B + EpExtra. Research extract = `accepted` and both readers. |
| This node | `bin/leo batch notes.xlsx --local` | GPU if CUDA is visible, otherwise CPU. The command says which. |

Weights, the concept database, and Slurm flags: [`LEO_HOSTING.md`](LEO_HOSTING.md).
