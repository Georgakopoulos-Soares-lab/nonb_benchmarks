#!/bin/bash
#SBATCH --job-name=ImGQfinder
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/g4/ImGQfinder/run_%a.out
#SBATCH --error=logs/g4/ImGQfinder/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}
SUBMIT_DIR=$(pwd)

FASTA="${SUBMIT_DIR}/data/chr18.fa"
OUTDIR="$(readlink -f -m results/g4/ImGQfinder/run_${RUN})"
OUTFILE="$OUTDIR/res.txt"
BENCH="${SUBMIT_DIR}/benchmarks/g4/ImGQfinder/run_${RUN}.txt"
IMGQFINDER="${SUBMIT_DIR}/src/g4/dependencies/ImGQfinder/imgqfinder.py"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"
trap 'rm -f "$JOB_FASTA"' EXIT

cd "$OUTDIR"

/usr/bin/time -v -o "$BENCH" \
    python3 \
    "$IMGQFINDER" \
    -i "$JOB_FASTA"