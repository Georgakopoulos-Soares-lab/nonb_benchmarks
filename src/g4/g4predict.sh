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

    OUTDIR="$ROOT/results/g4/g4predict/run_${RUN}"
    OUTFILE="$OUTDIR/res.bed"
    BENCH="$ROOT/benchmarks/g4/g4predict/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="$OUTDIR/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    ulimit -c unlimited

    cd "$OUTDIR"

    /usr/bin/time -v -o "$BENCH" \
        g4predict \
        intra \
        --fasta "$JOB_FASTA" \
        --bed "$OUTFILE" \
        --min-tetrad 3 \
        --max-tetrad 4 \
        --min-loop 1 \
        --max-loop 9 \
        --bulges 0
    
    rm -f "$JOB_FASTA"
done