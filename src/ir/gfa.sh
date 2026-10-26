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
    GFA="$ROOT/src/general/non-B_gfa/gfa"
    OUTDIR="$ROOT/results/ir/Non-B GFA IR/run_${RUN}"
    BENCH="$ROOT/benchmarks/ir/Non-B GFA IR/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cd "$OUTDIR"

    cp "$FASTA" "$JOB_FASTA"

    /usr/bin/time -v -o "$BENCH" \
        "$GFA" \
        -seq "$JOB_FASTA" \
        -out gfa_out \
        -skipAPR \
        -skipSTR \
        -skipDR \
        -skipMR \
        -skipZ \
        -skipGQ \
        -skipSlipped \
        -skipCruciform \
        -skipTriplex \
        -skipWGET \
        -minIRrep 10 \
        -maxIRspacer 100

done