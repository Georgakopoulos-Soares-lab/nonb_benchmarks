#!/bin/bash
#SBATCH --job-name=irf
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=spr
#SBATCH --account=BCS25105
#SBATCH --output=logs/ir/irf/run_%a.out
#SBATCH --error=logs/ir/irf/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$SUBMIT_DIR"

FASTA="$(readlink -f data/chr18.fa)"
IRF="$(readlink -f src/ir/dependencies/IRF/bin/irf.exe)"
OUTDIR="$(readlink -f -m results/ir/irf/run_${RUN})"
BENCH="$(readlink -f -m benchmarks/ir/irf/run_${RUN}.txt)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

ulimit -c unlimited

cd "$OUTDIR"
/usr/bin/time -v -o "$BENCH" \
    "$IRF" \
    "$JOB_FASTA" \
    2 3 5 80 10 20 100000 1000000 \
    -h \
    -d

rm "$JOB_FASTA"