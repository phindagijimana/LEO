# Research-host deploy (local, single-user)

**Required** so a note cannot leave this machine. **Optional** on `127.0.0.1`. Written IRB/IS approval is policy — send [LEO_IS_REQUEST.md](LEO_IS_REQUEST.md); it is not a code flag.

## Required (`--research` fails without these)

```bash
bin/leo check --research
bin/leo start --local --research
bin/leo batch notes.xlsx --research
```

Or `export MEDAI_LEO_RESEARCH=1`.

| Gate | Why |
|---|---|
| EpExtra CDB on disk | No fetch of the concept DB |
| Med42-8B in `model_cache/` | No Hugging Face download |
| `HF_HUB_OFFLINE` + `TRANSFORMERS_OFFLINE` | Loader uses `local_files_only` |
| No `MEDAI_LEO_BACKEND=openai` | Notes stay on the host |

Also keep outputs off git (`*_leo.csv`, `data/leo_jobs/`, reviews).

## Optional (reported as info)

| Item | When it matters |
|---|---|
| Web login (`bin/leo user add`) | **Required** if the UI binds a Slurm/node address. Skip on `127.0.0.1` if only you use the machine. |
| Job folders `0700` | Nice on group-readable NFS; not a fail. |
| `MEDAI_LEO_IRB_ACK=1` | Reminder only. Approval is the IS letter, not this variable. |

Synthetic smoke without `--research` is unchanged.

## Still not in the tool

Disk encryption (IS names the volume). Shipping Med42 or UMLS ([LEO_THIRD_PARTY.md](LEO_THIRD_PARTY.md)). Real-note F1 (held-out set after they approve the host).
