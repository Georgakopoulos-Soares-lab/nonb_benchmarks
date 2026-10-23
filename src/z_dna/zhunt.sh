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
    OUTDIR="$ROOT/results/z_dna/zhunt/run_${RUN}"
    BENCH="$ROOT/benchmarks/z_dna/zhunt/run_${RUN}.txt"
    ZHUNT="$ROOT/src/z_dna/dependencies/zhunt/bin/zhunt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    CLEAN_FASTA="${OUTDIR}/clean_chr18.fa"
    grep -v '^>' "$FASTA" | tr -d '\n' > "$CLEAN_FASTA"

    /usr/bin/time -v -o "$BENCH" \
        "$ZHUNT" 12 6 12 "$CLEAN_FASTA"

    rm "$CLEAN_FASTA"
done