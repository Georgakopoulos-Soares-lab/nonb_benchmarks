#!/bin/bash
#SBATCH --job-name=zhunt
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=spr
#SBATCH --account=BCS25105
#SBATCH --output=logs/zdna/zhunt/run_%a.out
#SBATCH --error=logs/zdna/zhunt/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/zdna/zhunt/run_${RUN}"
BENCH="benchmarks/zdna/zhunt/run_${RUN}.txt"
ZHUNT="src/z_dna/dependencies/zhunt/bin/zhunt"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

CLEAN_FASTA="${OUTDIR}/clean_chr18.fa"
grep -v '^>' "$FASTA" | tr -d '\n' > "$CLEAN_FASTA"

/usr/bin/time -v -o "$BENCH" \
    "$ZHUNT" 12 6 12 "$CLEAN_FASTA"

rm "$CLEAN_FASTA"
