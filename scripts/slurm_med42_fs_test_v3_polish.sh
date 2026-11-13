#!/bin/bash
#SBATCH --job-name=leo-fs-v3polish
#SBATCH --partition=interactive
#SBATCH --gres=gpu:l40s.24g:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=03:00:00
#SBATCH --output=logs/leo_fs_test_v3polish_%j.out
#SBATCH --error=logs/leo_fs_test_v3polish_%j.err
#
# Arm H (M4 v3 polish LoRA): Med42-8B + adapter on 40 held-out F-S letters.
#
# Submit:
#   sbatch scripts/slurm_med42_fs_test_v3_polish.sh
#
# After completion:
#   venv/bin/python scripts/score_llm_arms_vs_fs_gold.py \
#       --manifests-dir data/run_manifests_fs_test_tuned_v3_polish \
#       --held-out-only \
#       --suffix tuned_v3_polish_fs_test

set -euo pipefail

export LEO_MAX_NEW_TOKENS="${LEO_MAX_NEW_TOKENS:-4096}"
_SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
ADAPTER="${LEO_LORA_ADAPTER_DIR:-$_SUBMIT_DIR/checkpoints/llama3-med42-8b_lora_epi_v3_polish}"
export LEO_LORA_ADAPTER_DIR="$ADAPTER"
export LEO_MANIFEST_DIR="${LEO_MANIFEST_DIR:-$_SUBMIT_DIR/data/run_manifests_fs_test_tuned_v3_polish}"
export LEO_CONSTRAINED="${LEO_CONSTRAINED:-}"

exec bash "$_SUBMIT_DIR/scripts/slurm_med42_fs_test.sh"
