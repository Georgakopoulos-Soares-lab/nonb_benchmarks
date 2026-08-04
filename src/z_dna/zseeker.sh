#!/bin/bash
#SBATCH --job-name=zseeker
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/zdna/zseeker/slurm_run_%a.out
#SBATCH --error=logs/zdna/zseeker/slurm_run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}
FASTA="data/chr18.fa"
OUTDIR="results/z_dna/zseeker/run_${RUN}"
BENCH="benchmarks/z_dna/zseeker/run_${RUN}.txt"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

/usr/bin/time -v -o "$BENCH" \
    ZSeeker \
        --fasta "$JOB_FASTA" \
        --n_jobs 1 \
        --output_dir "$OUTDIR"