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
    OUTDIR="$ROOT/results/dr_and_str/Pytrf/run_${RUN}"
    OUTFILE="$OUTDIR/res.txt"
    BENCH="$ROOT/benchmarks/dr_and_str/Pytrf/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    cd "$OUTDIR"
    /usr/bin/time -v -o "$BENCH" \
        pytrf \
        findstr \
        -r 12 6 4 3 3 2 \
        --out-format tsv \
        --out-file "$OUTFILE" \
        "$JOB_FASTA"

    rm "$JOB_FASTA"

done