#!/bin/bash
#SBATCH --job-name=pqsfinder
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=spr
#SBATCH --account=BCS25105
#SBATCH --output=logs/g4/pqsfinder/run_%a.out
#SBATCH --error=logs/g4/pqsfinder/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/g4/pqsfinder/run_${RUN}"
OUTFILE="$OUTDIR/res.bed"
BENCH="benchmarks/g4/pqsfinder/run_${RUN}.txt"
PQSFINDER="src/g4/pqsfinder.R"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

/usr/bin/time -v -o "$BENCH" \
    Rscript \
    "$PQSFINDER" \
    "$JOB_FASTA" \
    "$OUTFILE"

rm "$JOB_FASTA"
