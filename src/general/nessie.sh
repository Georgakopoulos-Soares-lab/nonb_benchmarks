#!/bin/bash
#SBATCH --job-name=nessie
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/general/nessie/run_%a.out
#SBATCH --error=logs/general/nessie/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$SUBMIT_DIR"

FASTA="$(readlink -f data/chr18.fa)"
NESSIE="$(readlink -f src/general/dependencies/nessie/nessie)"
OUTDIR="$(readlink -f -m results/general/nessie/run_${RUN})"
OUTFILE="$OUTDIR/res.txt"
BENCH="$(readlink -f -m benchmarks/general/nessie/run_${RUN}.txt)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

#TIR detection

/usr/bin/time -v -o "$BENCH" \
    "$NESSIE" \
    -I "$JOB_FASTA" \
    -O "$OUTFILE" \
    -M -k 10

rm "$JOB_FASTA"