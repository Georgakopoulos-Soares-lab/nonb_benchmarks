#!/bin/bash
#SBATCH --job-name=quadron
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/g4/quadron/run_%a.out
#SBATCH --error=logs/g4/quadron/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/g4/quadron/run_${RUN}"
OUTFILE="$OUTDIR/res.bed"
BENCH="benchmarks/g4/quadron/run_${RUN}.txt"
QUADRON_LIB="src/g4/dependencies/Quadron/Quadron.lib"
QUADRON="src/g4/quadron.R"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

/usr/bin/time -v -o "$BENCH" \
    Rscript \
    "$QUADRON" \
    "$JOB_FASTA" \
    "$OUTFILE" \
    "$QUADRON_LIB"

rm "$JOB_FASTA"
