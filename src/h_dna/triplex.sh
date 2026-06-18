#!/bin/bash
#SBATCH --job-name=triplex
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=spr
#SBATCH --account=BCS25105
#SBATCH --output=logs/h_dna/triplex/run_%a.out
#SBATCH --error=logs/h_dna/triplex/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/h_dna/triplex/run_${RUN}"
OUTFILE="$OUTDIR/res.bed"
BENCH="benchmarks/h_dna/triplex/run_${RUN}.txt"
TRIPLEX="src/h_dna/triplex.R"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

/usr/bin/time -v -o "$BENCH" \
    Rscript \
    "$TRIPLEX" \
    "$JOB_FASTA" \
    "$OUTFILE"

rm "$JOB_FASTA"
