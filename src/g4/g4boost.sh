#!/bin/bash
#SBATCH --job-name=g4boost
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/g4/g4boost/run_%a.out
#SBATCH --error=logs/g4/g4boost/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}
SUBMIT_DIR=$(pwd)

FASTA="${SUBMIT_DIR}/data/chr18.fa"
OUTDIR="${SUBMIT_DIR}/results/g4/g4boost/run_${RUN}"
BENCH="${SUBMIT_DIR}/benchmarks/g4/g4boost/run_${RUN}.txt"
G4BOOST="${SUBMIT_DIR}/src/g4/dependencies/G4Boost/G4Boost_v4.py"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"
trap 'rm -f "$JOB_FASTA"' EXIT

cd "$OUTDIR"

/usr/bin/time -v -o "$BENCH" \
    python3 \
    "$G4BOOST" \
    --fasta "$JOB_FASTA" \
    -g 3
