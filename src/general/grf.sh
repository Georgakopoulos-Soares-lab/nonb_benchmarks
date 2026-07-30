#!/bin/bash
#SBATCH --job-name=grf
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=spr
#SBATCH --account=BCS25073
#SBATCH --output=logs/general/grf/run_%a.out
#SBATCH --error=logs/general/grf/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$SUBMIT_DIR"

FASTA="$(readlink -f data/chr18.fa)"
GRF="$(readlink -f src/general/dependencies/GenericRepeatFinder-1.0.2/src/grf-main/grf-main)"
OUTDIR="$(readlink -f -m results/general/grf/run_${RUN})"
BENCH="$(readlink -f -m benchmarks/general/grf/run_${RUN}.txt)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

#TIR detection

/usr/bin/time -v -o "$BENCH" \
    "$GRF" \
    -i "$JOB_FASTA" \
    -c 0 \
    -o "$OUTDIR" \
    --min_tr 10 \
    -t 1

rm "$JOB_FASTA"