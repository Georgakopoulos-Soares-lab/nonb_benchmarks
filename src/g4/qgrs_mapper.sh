#!/bin/bash
#SBATCH --job-name=qgrs_mapper
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/g4/qgrs_mapper/run_%a.out
#SBATCH --error=logs/g4/qgrs_mapper/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/g4/qgrs_mapper/run_${RUN}"
OUTFILE="$OUTDIR/res.csv"
BENCH="benchmarks/g4/qgrs_mapper/run_${RUN}.txt"
QGRSMAPPER="src/g4/dependencies/qgrs-cpp/qgrs"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

/usr/bin/time -v -o "$BENCH" \
    $QGRSMAPPER \
    -i "$JOB_FASTA" \
    -o "$OUTFILE"

rm "$JOB_FASTA"