#!/bin/bash
#SBATCH --job-name=hseeker
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/h_dna/hseeker/run_%a.out
#SBATCH --error=logs/h_dna/hseeker/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/h_dna/hseeker/run_${RUN}"
OUTPREFIX="$OUTDIR/res"
BENCH="benchmarks/h_dna/hseeker/run_${RUN}.txt"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

/usr/bin/time -v -o "$BENCH" \
    hseeker \
    -seq "$JOB_FASTA" \
    -out "$OUTPREFIX" \
    -workers 1

rm "$JOB_FASTA"
