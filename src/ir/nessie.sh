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
    NESSIE="$ROOT/src/ir/dependencies/nessie/nessie"
    OUTDIR="$ROOT/results/ir/NeSSie/run_${RUN}"
    OUTFILE="$OUTDIR/res.txt"
    BENCH="$ROOT/benchmarks/ir/NeSSie/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    /usr/bin/time -v -o "$BENCH" \
        "$NESSIE" \
        --input "$JOB_FASTA" \
        --output "$OUTFILE" \
        --palindrome \
        --kmin 20 \
        --kmax 900 \
        --MAX

    rm "$JOB_FASTA"
done