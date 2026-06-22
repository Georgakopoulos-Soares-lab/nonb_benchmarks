#!/bin/bash
#SBATCH --job-name=trf
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=spr
#SBATCH --account=BCS25105
#SBATCH --output=logs/dr_and_str/trf/run_%a.out
#SBATCH --error=logs/dr_and_str/trf/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$SUBMIT_DIR"

FASTA="$(readlink -f data/chr18.fa)"
OUTDIR="$(readlink -f -m results/dr_and_str/trf/run_${RUN})"
BENCH="$(readlink -f -m benchmarks/dr_and_str/trf/run_${RUN}.txt)"
TRF="$(readlink -f src/dr_and_str/dependencies/TRF/build/src/trf)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

ulimit -c unlimited

cd "$OUTDIR"
/usr/bin/time -v -o "$BENCH" \
    "$TRF" \
    "$JOB_FASTA" \
    2 7 7 80 10 50 500 \
    -f \
    -d \
    -m \
    -h

rm "$JOB_FASTA"
