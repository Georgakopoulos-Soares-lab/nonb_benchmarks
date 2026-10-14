#!/bin/bash
#SBATCH --job-name=iupacpal
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/ir/iupacpal/run_%a.out
#SBATCH --error=logs/ir/iupacpal/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$SUBMIT_DIR"

FASTA="$(readlink -f data/chr18.fa)"
IUPACPAL="$(readlink -f src/ir/dependencies/IUPACpal/IUPACpal)"
OUTDIR="$(readlink -f -m results/ir/iupacpal/run_${RUN})"
BENCH="$(readlink -f -m benchmarks/ir/iupacpal/run_${RUN}.txt)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

ulimit -c unlimited

cd "$OUTDIR"
/usr/bin/time -v -o "$BENCH" \
    "$IUPACPAL" \
    -f "$JOB_FASTA" \
    -s chr18

rm "$JOB_FASTA"