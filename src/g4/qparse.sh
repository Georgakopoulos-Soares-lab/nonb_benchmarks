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
    OUTDIR="$ROOT/results/g4/QPARSE/run_${RUN}"
    OUTFILE="$OUTDIR/res.txt"
    BENCH="$ROOT/benchmarks/g4/QPARSE/run_${RUN}.txt"
    QPARSE="$ROOT/src/g4/dependencies/qparse/QPARSE_1.10.py"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="$OUTDIR/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"
    
    ulimit -c unlimited

    cd "$OUTDIR"

    /usr/bin/time -v -o "$BENCH" \
        python3 \
        "$QPARSE" \
        --inputsequence "$JOB_FASTA" \
        --output "$OUTFILE" \
        --minlen 3 \
        --maxlen 4 \
        --maxloop 9 

    rm "$JOB_FASTA"
done