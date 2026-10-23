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

    IUPACPAL="$ROOT/src/ir/dependencies/IUPACpal/IUPACpal"
    OUTDIR="$ROOT/results/ir/iupacpal/run_${RUN}"
    OUTFILE="$OUTDIR/perfect.out"
    BENCH="$ROOT/benchmarks/ir/iupacpal/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    ulimit -c unlimited

    cd "$OUTDIR"
    /usr/bin/time -v -o "$BENCH" \
        "$IUPACPAL" \
        -f "$JOB_FASTA" \
        -s NC_060942.1 \
        -m 10 \
        -M 450 \
        -g 100 \
        -x 0 \
        -o "$OUTFILE"

    rm "$JOB_FASTA"

done