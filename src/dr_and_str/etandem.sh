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
    OUTDIR="$ROOT/results/dr_and_str/Etandem/run_${RUN}"
    BENCH="$ROOT/benchmarks/dr_and_str/Etandem/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    /usr/bin/time -v -o "$BENCH" \
        etandem \
        -sequence "$JOB_FASTA" \
        -minrepeat 2 \
        -maxrepeat 6 \
        -threshold 6 \
        -outfile "$OUTDIR/res.etandem" 

done