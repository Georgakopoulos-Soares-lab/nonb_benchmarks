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

FASTA="data/chr18.fa"
OUTDIR="results/dr_and_str/trf/run_${RUN}"
BENCH="benchmarks/dr_and_str/trf/run_${RUN}.txt"
TRF="src/dr_and_str/dependencies/TRF/build/src/trf"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

ulimit -c unlimited

/usr/bin/time -v -o "$BENCH" \
    "$TRF" "$JOB_FASTA" 2 7 7 80 10 50 500 -f -d -m -h -ngs

rm "$JOB_FASTA"
