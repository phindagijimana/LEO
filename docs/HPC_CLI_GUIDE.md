# HPC

LEO on a cluster is `bin/leo`, not a separate HPC binary.

Login node, no GPU: `bin/leo check --slurm` and `bin/leo batch notes.xlsx` submit a GPU job. `--cpu` is rules only; every cell needs review. `--local` stays on the current node.

Partition, GRES, and memory: [`LEO_HOSTING.md`](LEO_HOSTING.md). Real notes: [`LEO_RESEARCH_DEPLOY.md`](LEO_RESEARCH_DEPLOY.md).
