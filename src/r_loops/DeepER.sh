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

    DEEPER="$ROOT/src/r_loops/dependencies/DeepER/DeepER-deploy/Script.py"
    MODEL="$ROOT/src/r_loops/dependencies/DeepER/DeepER-deploy/DeepER.pkl"
    OUTDIR="$ROOT/results/r_loops/DeepER/run_${RUN}"
    OUTFILE="$OUTDIR/res.txt"
    BENCH="$ROOT/benchmarks/r_loops/DeepER/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    awk '/^>/ {print; next} {print toupper($0)}' "$FASTA" > "$JOB_FASTA"

    cd "$OUTDIR"
    /usr/bin/time -v -o "$BENCH" \
        python \
        "$DEEPER" \
        "$JOB_FASTA" \
        "$MODEL" \
        forward \
        "$OUTFILE" \
        1

    rm "$JOB_FASTA"

done
