# LEO research extract — code only. Mount Med42 weights and the MedCAT CDB at run time.
# Licenses forbid baking those into the image (docs/LEO_THIRD_PARTY.md).
#
#   docker build -f Dockerfile.leo -t leo:research .
#   docker compose -f docker-compose.leo.yml up
#
# GPU extract needs the NVIDIA Container Toolkit and a 24 GB GPU.
# Bind the published port to 127.0.0.1 on the host (see compose).

# CUDA libraries come from the pinned pip wheels (cu130); the host driver comes from the NVIDIA toolkit.
# Ubuntu 22.04's python3.11 is 3.11.0rc1, which breaks torch 2.14; use a current 3.11.
FROM docker.io/library/python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive \
    HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1 \
    HF_HUB_DISABLE_TELEMETRY=1 \
    MEDAI_LEO_BLOCK_CLOUD=1 \
    SERVICE_HOST=0.0.0.0 \
    SERVICE_PORT=8085 \
    MEDAI_LOAD_MED42=1 \
    MEDAI_REQUIRE_GPU=1 \
    MEDAI_EAGER_LOAD=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements-leo.lock.txt gunicorn_config.py app.py ./
COPY bin/leo bin/leo
COPY scripts/leo_cli.py scripts/__init__.py scripts/enrich_ontology_from_epio.py scripts/
COPY services/ services/
COPY routes/ routes/
COPY schema/ schema/
COPY rules/ rules/
COPY data/ontologies/MANIFEST.json data/ontologies/MANIFEST.json
COPY data/guidelines data/guidelines

RUN python3.11 -m venv /app/venv-medcat \
    && /app/venv-medcat/bin/pip install --upgrade pip \
    && /app/venv-medcat/bin/pip install --no-deps \
        --extra-index-url https://download.pytorch.org/whl/cu130 \
        -r requirements-leo.lock.txt \
    && chmod +x /app/bin/leo \
    && mkdir -p /app/logs /app/data/leo_jobs /app/data/leo_training /app/model_cache \
    && chmod 0700 /app/data/leo_jobs /app/data/leo_training

EXPOSE 8085

# Host maps 127.0.0.1:8085 → this port. Weights and CDB must be mounted.
ENTRYPOINT ["/app/bin/leo"]
CMD ["start", "--local", "--port", "8085", "--research"]
