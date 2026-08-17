#!/bin/bash
#SBATCH --job-name=zhunt
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/z_dna/zhunt/run_%a.out
#SBATCH --error=logs/z_dna/zhunt/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/z_dna/zhunt/run_${RUN}"
BENCH="benchmarks/z_dna/zhunt/run_${RUN}.txt"
ZHUNT="src/z_dna/dependencies/zhunt/bin/zhunt"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

CLEAN_FASTA="${OUTDIR}/clean_chr18.fa"
grep -v '^>' "$FASTA" | tr -d '\n' > "$CLEAN_FASTA"

/usr/bin/time -v -o "$BENCH" \
    "$ZHUNT" 12 6 12 "$CLEAN_FASTA"

rm "$CLEAN_FASTA"
