# Container (LEO research extract)

Yes — the **code** can live in a container. Med42 weights and the UMLS/MedCAT CDB **cannot** (licenses). You mount them. The existing `Dockerfile` / `Dockerfile.gpu` are the old `/extract` app and were not tested for LEO. Use these instead.

## What the image is

| In the image | On the host (mount) |
|---|---|
| Python 3.11, `venv-medcat`, `requirements-leo.txt`, spaCy `en_core_web_sm` | `model_cache/models--m42-health--Llama3-Med42-8B` |
| `bin/leo`, Flask `/leo/ui`, gunicorn | `data/medcat_cdb_epilepsy/cdb` |
| Offline env (`HF_HUB_OFFLINE`, no cloud LLM) | `.env` (`UMLS_API_KEY` only; never in the image) |
| | Job outputs: `data/leo_jobs/` |

Host publish is **`127.0.0.1:8085`**. Inside the container gunicorn binds `0.0.0.0` (Docker port publish requires that). Login is optional if only you can reach that loopback port.

## Workstation (Docker + GPU)

```bash
# once: weights + CDB already on disk; .env present
docker compose -f docker-compose.leo.yml build
docker compose -f docker-compose.leo.yml up
# UI: http://127.0.0.1:8085/leo/ui

# batch one spreadsheet (synthetic unless IS/IRB said yes)
docker compose -f docker-compose.leo.yml run --rm \
  -v "$PWD/notes.xlsx:/data/notes.xlsx:ro" \
  -v "$PWD:/data/out" \
  leo batch /data/notes.xlsx -o /data/out/notes_leo.xlsx --local --research
```

Needs the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) and a ~24 GB GPU.

## Slurm (Apptainer / Singularity)

Docker daemons are often banned on HPC, and rootless Podman needs `/etc/subuid` ranges. `leo.def` builds the same image with Apptainer, no Docker needed:

```bash
apptainer build --fakeroot leo.sif leo.def

apptainer exec --nv \
  --bind "$PWD/model_cache:/app/model_cache:ro" \
  --bind "$PWD/data/medcat_cdb_epilepsy:/app/data/medcat_cdb_epilepsy:ro" \
  --bind "$PWD/.env:/app/.env:ro" \
  --bind "$PWD/data/leo_jobs:/app/data/leo_jobs" \
  --bind "$PWD/logs:/app/logs" \
  leo.sif /app/bin/leo batch notes.xlsx --local --research
```

The `.sif` is read-only; bind a writable jobs folder and `logs/`. `leo.sif` is gitignored. If you already have a Docker image: `apptainer build leo.sif docker-daemon://leo:research`.

## What we do not put in the image

Med42, UMLS, CDB, `.env`, notes, `*_leo.csv` ([LEO_THIRD_PARTY.md](LEO_THIRD_PARTY.md)). `.dockerignore` excludes those so `COPY` cannot bake PHI.

CPU-only container = rules only; every cell `needs_review`. Not a research extract.

## Check

```bash
docker compose -f docker-compose.leo.yml run --rm leo check --research
```

Weights missing → fail (offline; it will not download).

`bin/leo phi-scan` is in the image. It is a warning, not de-identification ([LEO_PHI.md](LEO_PHI.md)).
