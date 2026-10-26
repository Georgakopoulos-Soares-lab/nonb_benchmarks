#!/bin/bash

set -euo pipefail

module load matlab

NRUNS=${1:-1}

if ! [[ "$NRUNS" =~ ^[1-9][0-9]*$ ]]; then
    echo "Usage: $0 [NRUNS]  (NRUNS must be a positive integer)" >&2
    exit 1
fi

ROOT="$(pwd)"

FASTA="$ROOT/data/chr18.fa"

for RUN in $(seq 1 "$NRUNS"); do
    DETECTIR="$ROOT/src/ir/detectIR.m"
    OUTDIR="$ROOT/results/ir/DetectIR/run_${RUN}"
    BENCH="$ROOT/benchmarks/ir/DetectIR/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    export IR_FUNCDIR="$ROOT/src/ir/dependencies/detectIR"
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
done