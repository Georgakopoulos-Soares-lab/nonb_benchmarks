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
    OUTDIR="$ROOT/results/g4/Quadron/run_${RUN}"
    OUTFILE="$OUTDIR/res.bed"
    BENCH="$ROOT/benchmarks/g4/Quadron/run_${RUN}.txt"
    QUADRON_LIB="$ROOT/src/g4/dependencies/Quadron/Quadron.lib"
    QUADRON="$ROOT/src/g4/quadron.R"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"
    
    ulimit -c unlimited

    /usr/bin/time -v -o "$BENCH" \
        Rscript \
        "$QUADRON" \
        "$JOB_FASTA" \
        "$OUTFILE" \
        "$QUADRON_LIB"

    rm "$JOB_FASTA"

done