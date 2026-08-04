#!/bin/bash
#SBATCH --job-name=matlabir
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/ir/matlabir/run_%a.out
#SBATCH --error=logs/ir/matlabir/run_%a.err

module load matlab
set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$SUBMIT_DIR"

FASTA="$(readlink -f data/chr18.fa)"
MATLABIR="$(readlink -f src/ir/matlabIR.m)"
OUTDIR="$(readlink -f -m results/ir/matlabir/run_${RUN})"
BENCH="$(readlink -f -m benchmarks/ir/matlabir/run_${RUN}.txt)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

export IR_FUNCDIR="$(readlink -f src/ir/dependencies/MATLAB_IR)"
export IR_INPUT="$JOB_FASTA"
export IR_OUTPUT="$OUTDIR/predictedIRs.fasta"

/usr/bin/time -v -o "$BENCH" \
    matlab \
    -nodesktop \
    -nosplash < "$MATLABIR"

rm "$JOB_FASTA"