#!/bin/bash

set -euo pipefail

NRUNS=${1:-1}

if ! [[ "$NRUNS" =~ ^[1-9][0-9]*$ ]]; then
    echo "Usage: $0 [NRUNS]  (NRUNS must be a positive integer)" >&2
    exit 1
fi

ROOT="$(pwd)"

FASTA="$ROOT/data/chr18.fa"

for RUN in $(seq 1 "$NRUNS"); do
    OUTDIR="$ROOT/results/g4/G4Hunter/run_${RUN}"
    BENCH="$ROOT/benchmarks/g4/G4Hunter/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    /usr/bin/time -v -o "$BENCH" \
        g4hunter \
        --window-size 25 \
        --min_score 1.5 \
        --min-loop-length 1 \
        --max-loop-length 9 \
        --outdir "$OUTDIR" \
        "$JOB_FASTA" 

    rm "$JOB_FASTA"
done