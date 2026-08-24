#!/bin/bash
#SBATCH --job-name=g4_imgrinder
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/g4/g4_imgrinder/run_%a.out
#SBATCH --error=logs/g4/g4_imgrinder/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/g4/g4_imgrinder/run_${RUN}"
OUTFILE="$OUTDIR/res.csv"
BENCH="benchmarks/g4/g4_imgrinder/run_${RUN}.txt"
G4_IMGRINDER="src/g4/g4_imgrinder.R"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

/usr/bin/time -v -o "$BENCH" \
    Rscript \
    "$G4_IMGRINDER" \
    "$JOB_FASTA" \
    "$OUTFILE"

rm "$JOB_FASTA"
