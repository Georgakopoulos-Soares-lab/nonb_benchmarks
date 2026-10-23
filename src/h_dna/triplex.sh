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
    OUTDIR="$ROOT/results/h_dna/triplex/run_${RUN}"
    OUTFILE="$OUTDIR/res.bed"
    BENCH="$ROOT/benchmarks/h_dna/triplex/run_${RUN}.txt"
    TRIPLEX="$ROOT/src/h_dna/triplex.R"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    /usr/bin/time -v -o "$BENCH" \
        Rscript \
        "$TRIPLEX" \
        "$JOB_FASTA" \
        "$OUTFILE"

    rm "$JOB_FASTA"

done