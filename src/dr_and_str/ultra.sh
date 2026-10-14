#!/bin/bash
#SBATCH --job-name=ULTRA
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/dr_and_str/ULTRA/run_%a.out
#SBATCH --error=logs/dr_and_str/ULTRA/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$SUBMIT_DIR"

FASTA="$(readlink -f data/chr18.fa)"
ULTRA="$(readlink -f src/dr_and_str/dependencies/ULTRA/ultra)"
OUTDIR="$(readlink -f -m results/dr_and_str/ULTRA/run_${RUN})"
BENCH="$(readlink -f -m benchmarks/dr_and_str/ULTRA/run_${RUN}.txt)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

cd "$OUTDIR"
/usr/bin/time -v -o "$BENCH" \
    "$ULTRA" \
    --threads 1 \
    "$JOB_FASTA"

rm "$JOB_FASTA"