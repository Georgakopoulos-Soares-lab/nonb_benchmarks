#!/bin/bash
#SBATCH --job-name=detectir
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=spr
#SBATCH --account=BCS25105
#SBATCH --output=logs/ir/detectir/run_%a.out
#SBATCH --error=logs/ir/detectir/run_%a.err

module load matlab
set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$SUBMIT_DIR"

FASTA="$(readlink -f data/chr18.fa)"
DETECTIR="$(readlink -f src/ir/detectIR.m)"
OUTDIR="$(readlink -f -m results/ir/detectir/run_${RUN})"
BENCH="$(readlink -f -m benchmarks/ir/detectir/run_${RUN}.txt)"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

export IR_INPUT="$JOB_FASTA"
export IR_PERF_OUT="$OUTDIR/perfect_repeats.fasta"
export IR_PERF_RUN="$OUTDIR/perfect_repeats.runtime"
export IR_IMPERF_OUT="$OUTDIR/imperfect_repeats.fasta"
export IR_IMPERF_RUN="$OUTDIR/imperfect_repeats.runtime"

/usr/bin/time -v -o "$BENCH" \
    matlab \
    -nodesktop \
    -nosplash < "$DETECTIR"

rm "$JOB_FASTA"