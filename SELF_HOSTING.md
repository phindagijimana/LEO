# Self-hosting

Install and run LEO on a machine you control:

```bash
bin/leo install --check-only
bin/leo check
bin/leo start --local          # http://127.0.0.1  →  /leo/ui
```

A GPU extract from a login node is `bin/leo batch notes.xlsx` or `bin/leo start` (Slurm). Details: [`docs/LEO_HOSTING.md`](docs/LEO_HOSTING.md) and [`docs/LEO_LOCAL_DEPLOYMENT.md`](docs/LEO_LOCAL_DEPLOYMENT.md).
