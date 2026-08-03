#!/bin/bash
#SBATCH --job-name=triplexfpp
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/h_dna/triplexfpp/run_%a.out
#SBATCH --error=logs/h_dna/triplexfpp/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/h_dna/triplexfpp/run_${RUN}"
OUTFILE="$OUTDIR/res.bed"
BENCH="benchmarks/h_dna/triplexfpp/run_${RUN}.txt"
TRIPLEXFPP_LIB="src/h_dna/dependencies/TriplexFPP/code"
TRIPLEXFPP="src/h_dna/triplexfpp.py"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

/usr/bin/time -v -o "$BENCH" \
    python \
    "$TRIPLEXFPP" \
    --triplex-lib "$TRIPLEXFPP_LIB" \
    --data-path "$OUTDIR" \
    --input-file "$JOB_FASTA" \
    --output-file "$OUTFILE"

rm "$JOB_FASTA"
