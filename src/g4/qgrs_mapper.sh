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

    OUTDIR="$ROOT/results/g4/QGRS Mapper/run_${RUN}"
    OUTFILE="$OUTDIR/res.csv"
    BENCH="$ROOT/benchmarks/g4/QGRS Mapper/run_${RUN}.txt"
    QGRSMAPPER="$ROOT/src/g4/dependencies/qgrs-cpp/qgrs"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    ulimit -c unlimited

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    /usr/bin/time -v -o "$BENCH" \
        $QGRSMAPPER \
        -i "$JOB_FASTA" \
        -csv \
        -t 3 \
        -o "$OUTFILE"

    rm "$JOB_FASTA"

done