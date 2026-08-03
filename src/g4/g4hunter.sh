#!/bin/bash
#SBATCH --job-name=g4hunter
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/g4/g4hunter/run_%a.out
#SBATCH --error=logs/g4/g4hunter/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/g4/g4hunter/run_${RUN}"
BENCH="benchmarks/g4/g4hunter/run_${RUN}.txt"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

/usr/bin/time -v -o "$BENCH" \
    g4hunter \
    --outdir "$OUTDIR" \
    "$JOB_FASTA" 

rm "$JOB_FASTA"