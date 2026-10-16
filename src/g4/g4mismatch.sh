#!/bin/bash
#SBATCH --job-name=G4mismatch
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/g4/G4mismatch/run_%a.out
#SBATCH --error=logs/g4/G4mismatch/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="$(readlink -f data/chr18.fa)"
OUTDIR="$(readlink -f -m results/g4/G4mismatch/run_${RUN})"
BENCH="$(readlink -f -m benchmarks/g4/G4mismatch/run_${RUN}.txt)"
G4MISMATCH="$(readlink -f -m src/g4/dependencies/G4mismatch/G4mismatch_scan.py)"
MODEL="$(readlink -f -m src/g4/dependencies/G4mismatch/models/model_KPDS.h5)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

ulimit -c unlimited

cd "$OUTDIR"
/usr/bin/time -v -o "$BENCH" \
    python \
    "$G4CATCHALL" \
    --fasta "$JOB_FASTA"

python "$G4MISMATCH" \
    -dp "$JOB_FASTA" \
    -mp "$MODEL" \
    -of "$OUTDIR" \
    -m 1 \
    -fb 14.4 \
    -bs 128

rm "$JOB_FASTA"