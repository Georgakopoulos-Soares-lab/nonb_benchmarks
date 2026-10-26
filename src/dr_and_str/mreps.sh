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
    MREPS="$ROOT/src/dr_and_str/dependencies/mreps/mreps"
    OUTDIR="$ROOT/results/dr_and_str/Mreps/run_${RUN}"
    BENCH="$ROOT/benchmarks/dr_and_str/Mreps/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    cd "$OUTDIR"
    /usr/bin/time -v -o "$BENCH" \
        "$MREPS" \
        -fasta \
        -xmloutput "$OUTDIR/res.xml" \
        -minperiod 1 \
        -maxperiod 6 \
        -minsize 12 \
        "$JOB_FASTA"

    rm "$JOB_FASTA"
done