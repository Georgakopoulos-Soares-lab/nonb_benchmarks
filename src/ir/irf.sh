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

    IRF="$ROOT/src/ir/dependencies/IRF/bin/irf.exe"
    OUTDIR="$ROOT/results/ir/IRF/run_${RUN}"
    BENCH="$ROOT/benchmarks/ir/IRF/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    ulimit -c unlimited

    cd "$OUTDIR"

    /usr/bin/time -v -o "$BENCH" \
        "$IRF" \
        "$JOB_FASTA" \
        2 3 5 80 10 20 10000 101 \
        -h \
        -d

    rm "$JOB_FASTA"

done