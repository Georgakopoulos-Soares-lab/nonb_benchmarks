#!/bin/bash
#SBATCH --job-name=nonB_gfa
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=spr
#SBATCH --account=BCS25073
#SBATCH --output=logs/general/nonB_gfa/run_%a.out
#SBATCH --error=logs/general/nonB_gfa/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$SUBMIT_DIR"

FASTA="$(readlink -f data/chr18.fa)"
GFA="$(readlink -f src/general/dependencies/non-B_gfa/gfa)"
OUTDIR="$(readlink -f -m results/general/gfa/run_${RUN})"
BENCH="$(readlink -f -m benchmarks/general/gfa/run_${RUN}.txt)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cd "$OUTDIR"

trap 'rm -f "${OUTDIR}/clean_chr18.fa"' EXIT
cp "$FASTA" clean_chr18.fa

/usr/bin/time -v -o "$BENCH" \
    "$GFA" \
    -seq clean_chr18.fa \
    -out gfa_out \
    -skipAPR