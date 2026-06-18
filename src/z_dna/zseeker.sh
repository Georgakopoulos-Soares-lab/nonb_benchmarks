#!/bin/bash
#SBATCH --job-name=zseeker
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=spr
#SBATCH --account=BCS25105
#SBATCH --output=logs/zdna/zseeker/slurm_run_%a.out
#SBATCH --error=logs/zdna/zseeker/slurm_run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}
FASTA="data/chr18.fa"
OUTDIR="results/z_dna/zseeker/run_${RUN}"
BENCH="benchmarks/z_dna/zseeker/run_${RUN}.txt"

mkdir -p "$(dirname "$BENCH")"

/usr/bin/time -v -o "$BENCH" \
    ZSeeker \
        --fasta "$FASTA" \
        --n_jobs 1 \
        --output_dir "$OUTDIR"