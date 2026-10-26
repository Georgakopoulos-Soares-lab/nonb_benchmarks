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
    OUTDIR="$ROOT/results/dr_and_str/TRF/run_${RUN}"
    BENCH="$ROOT/benchmarks/dr_and_str/TRF/run_${RUN}.txt"
    TRF="$ROOT/src/dr_and_str/dependencies/TRF/build/src/trf"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    ulimit -c unlimited

    cd "$OUTDIR"

    /usr/bin/time -v -o "$BENCH" \
        "$TRF" \
        "$JOB_FASTA" \
        2 7 7 80 10 24 6 \
        -f \
        -h \
        -d \
        -ngs

    rm "$JOB_FASTA"
done

 -d \
    -m \
    -h