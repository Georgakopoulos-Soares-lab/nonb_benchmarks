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
    OUTDIR="$ROOT/results/g4/ImGQfinder/run_${RUN}"
    OUTFILE="$OUTDIR/res.txt"
    BENCH="$ROOT/benchmarks/g4/ImGQfinder/run_${RUN}.txt"
    IMGQFINDER="$ROOT/src/g4/dependencies/ImGQfinder/imgqfinder.py"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="$OUTDIR/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    ulimit -c unlimited

    cd "$OUTDIR"

    /usr/bin/time -v -o "$BENCH" \
        python3 \
        "$IMGQFINDER" \
        --input "$JOB_FASTA" \
        --output "$OUTDIR" \
        -L 9 \
        -mdef 0 \
        -maxbulge 0 \
        -tetdef 0 \
        --nthreads 1 \
        --repeats \
        --output_type 1

    rm -f "$JOB_FASTA"

done