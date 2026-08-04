#!/bin/bash
#SBATCH --job-name=einverted
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/general/einverted/run_%a.out
#SBATCH --error=logs/general/einverted/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$SUBMIT_DIR"

FASTA="$(readlink -f data/chr18.fa)"
OUTDIR="$(readlink -f -m results/general/einverted/run_${RUN})"
BENCH="$(readlink -f -m benchmarks/general/einverted/run_${RUN}.txt)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

/usr/bin/time -v -o "$BENCH" \
    einverted \
    -sequence "$JOB_FASTA"\
    -gap 12 \
    -threshold  50 \
    -match 3 \
    -mismatch -4 \
    -outfile "$OUTDIR/res.einverted" \
    -outseq  "$OUTDIR/res.inv.fa"