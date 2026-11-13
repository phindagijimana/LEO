#!/bin/bash
#SBATCH --job-name=leo-h2-eval
#SBATCH --partition=interactive
#SBATCH --gres=gpu:l40s.24g:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=logs/leo_h2_eval_%j.out
#SBATCH --error=logs/leo_h2_eval_%j.err
#
# Arm H2 (flat contract, adapter trained on verbatim spans, schema-constrained decoding, zero-shot
# prompt L0 = the prompt it was trained on).  Resumable and shardable.
#   WHAT=fs                                         F-S held-out letters EA0161-EA0200
#   WHAT=synth SYNTH_SET=eval|ext|v1v2              synthetic notes (services/synth_eval.py)
# e.g. sbatch --export=ALL,WHAT=synth,SYNTH_SET=ext,LEO_SHARD=0/4 scripts/slurm_med42_h2_eval.sh
set -euo pipefail
_SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$_SUBMIT_DIR"
if [ -f .env ]; then set -a; . ./.env; set +a; fi
export APP_HOME="$_SUBMIT_DIR" PYTHONNOUSERSITE=1
export LEO_LORA_ADAPTER_DIR="$_SUBMIT_DIR/checkpoints/llama3-med42-8b_lora_epi_h2"
export LEO_FLAT_ADAPTER_OK=1 LEO_ARMS=L0C
[ -d "$LEO_LORA_ADAPTER_DIR" ] || { echo "adapter missing: train H2 first" >&2; exit 1; }
echo "job=${SLURM_JOB_ID:-local} node=${SLURM_NODELIST:-$(hostname)} start=$(date) what=${WHAT:-fs} shard=${LEO_SHARD:-all}"
if [ "${WHAT:-fs}" = "fs" ]; then
  LEO_MANIFEST_DIR="$_SUBMIT_DIR/data/run_manifests_fs_test_h2" venv/bin/python scripts/run_med42_flat_on_fs_test.py
else
  export LEO_CORPUS=synth LEO_SYNTH_SET="${SYNTH_SET:-eval}"
  case "$LEO_SYNTH_SET" in eval) SFX="";; ext) SFX="_ext";; v1v2) SFX="_v1v2";; *) echo bad set >&2; exit 1;; esac
  LEO_MANIFEST_DIR="$_SUBMIT_DIR/data/run_manifests_synth_eval_h2${SFX}" venv/bin/python scripts/run_med42_flat_on_fs_test.py
fi
echo "finished=$(date)"
