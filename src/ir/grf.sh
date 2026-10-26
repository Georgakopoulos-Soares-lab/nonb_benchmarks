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
    GRF="$ROOT/src/ir/dependencies/GenericRepeatFinder/bin/grf-main"
    OUTDIR="$ROOT/results/ir/GRF/run_${RUN}"
    BENCH="$ROOT/benchmarks/ir/GRF/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    /usr/bin/time -v -o "$BENCH" \
        "$GRF" \
        -i "$JOB_FASTA" \
        -c 0 \
        -t 1 \
        -f 0 \
        --min_tr 10 \
        --max_tr 450 \
        --min_spacer_len 0 \
        --max_spacer_len 100 \
        --max_indel 0 \
        --max_mismatch 0 \
        --seed_mismatch 0 \
        -o "$OUTDIR"
        
    rm "$JOB_FASTA"

done