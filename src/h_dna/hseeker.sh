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

    OUTDIR="$ROOT/results/h_dna/HSeeker/run_${RUN}"
    OUTPREFIX="$OUTDIR/res"
    BENCH="$ROOT/benchmarks/h_dna/HSeeker/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    /usr/bin/time -v -o "$BENCH" \
        hseeker \
        -seq "$JOB_FASTA" \
        -out "$OUTPREFIX" \
        -workers 1 \
        -minrep 10 \
        -maxrep 30 \
        -maxspacer 10

    rm "$JOB_FASTA"

done