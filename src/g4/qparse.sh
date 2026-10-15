#!/bin/bash
#SBATCH --job-name=QPARSE
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/g4/QPARSE/run_%a.out
#SBATCH --error=logs/g4/QPARSE/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}
SUBMIT_DIR=$(pwd)

FASTA="${SUBMIT_DIR}/data/chr18.fa"
OUTDIR="$(readlink -f -m results/g4/QPARSE/run_${RUN})"
OUTFILE="$OUTDIR/res.txt"
BENCH="${SUBMIT_DIR}/benchmarks/g4/QPARSE/run_${RUN}.txt"
QPARSE="${SUBMIT_DIR}/src/g4/dependencies/qparse/QPARSE_1.10.py"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"
trap 'rm -f "$JOB_FASTA"' EXIT

cd "$OUTDIR"

/usr/bin/time -v -o "$BENCH" \
    python3 \
    "$QPARSE" \
    -i "$JOB_FASTA" \
    -o "$OUTFILE"