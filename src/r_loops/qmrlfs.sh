#!/bin/bash
#SBATCH --job-name=qmrlfs_finder
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/r_loops/qmrlfs_finder/run_%a.out
#SBATCH --error=logs/r_loops/qmrlfs_finder/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$SUBMIT_DIR"

FASTA="$(readlink -f data/chr18.fa)"
QMRLFS_FINDER="$(readlink -f src/r_loops/dependencies/QmRLFS-finder/QmRLFS-finder.py)"
OUTDIR="$(readlink -f -m results/r_loops/qmrlfs_finder/run_${RUN})"
BENCH="$(readlink -f -m benchmarks/r_loops/qmrlfs_finder/run_${RUN}.txt)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

cd "$OUTDIR"
/usr/bin/time -v -o "$BENCH" \
    python \
    "$QMRLFS_FINDER" \
    -i "$JOB_FASTA" \
    -o "$OUTDIR/res.tsv"

rm "$JOB_FASTA"