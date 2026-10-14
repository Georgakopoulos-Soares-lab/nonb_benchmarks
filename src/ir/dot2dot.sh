#!/bin/bash
#SBATCH --job-name=Dot2dot
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/dr_and_str/Dot2dot/run_%a.out
#SBATCH --error=logs/dr_and_str/Dot2dot/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$SUBMIT_DIR"

FASTA="$(readlink -f data/chr18.fa)"
DOT2DOT="$(readlink -f src/dr_and_str/dependencies/Dot2dot/executables/dot.linux)"
OUTDIR="$(readlink -f -m results/dr_and_str/Dot2dot/run_${RUN})"
BENCH="$(readlink -f -m benchmarks/dr_and_str/Dot2dot/run_${RUN}.txt)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

cd "$OUTDIR"
/usr/bin/time -v -o "$BENCH" \
    "$DOT2DOT" \
    --threads 1 \
    --sequence "$JOB_FASTA"

rm "$JOB_FASTA"