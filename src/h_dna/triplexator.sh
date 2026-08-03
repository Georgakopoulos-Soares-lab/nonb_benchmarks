#!/bin/bash
#SBATCH --job-name=triplexator
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/h_dna/triplexator/run_%a.out
#SBATCH --error=logs/h_dna/triplexator/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/h_dna/triplexator/run_${RUN}"
OUTFILE="$OUTDIR/res.bed"
BENCH="benchmarks/h_dna/triplexator/run_${RUN}.txt"
TRIPLEXATOR="src/h_dna/dependencies/triplexator/bin/triplexator"

mkdir -p "$OUTDIR" "tmp_$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

/usr/bin/time -v -o "$BENCH" \
    "$TRIPLEXATOR" \
    --duplex-file "$JOB_FASTA" \
    --output "$OUTFILE" \
    --output-format 0 \
    --runtime-mode 0 \
    --processors 1

rm "$JOB_FASTA"
