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
    MATLABIR="$ROOT/src/ir/findIR.m"
    OUTDIR="$ROOT/results/ir/findIR/run_${RUN}"
    BENCH="$ROOT/benchmarks/ir/findIR/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    export IR_FUNCDIR="$ROOT/src/ir/dependencies/findIR"
    export IR_INPUT="$JOB_FASTA"
    export IR_OUTPUT="$OUTDIR/predictedIRs.fasta"

    /usr/bin/time -v -o "$BENCH" \
        matlab \
        -nodesktop \
        -nosplash < "$MATLABIR"

    rm "$JOB_FASTA"

done