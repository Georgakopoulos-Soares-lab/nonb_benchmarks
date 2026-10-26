#!/bin/bash

set -euo pipefail

NRUNS=${1:-1}

if ! [[ "$NRUNS" =~ ^[1-9][0-9]*$ ]]; then
    echo "Usage: $0 [NRUNS]  (NRUNS must be a positive integer)" >&2
    exit 1
fi

FASTA="data/chr18.fa"
G4_IMGRINDER="src/g4/g4_imgrinder.R"

for RUN in $(seq 1 "$NRUNS"); do

    OUTDIR="results/g4/G4-iM Grinder/run_${RUN}"
    OUTFILE="$OUTDIR/res.csv"
    BENCH="benchmarks/g4/G4-iM Grinder/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    /usr/bin/time -v -o "$BENCH" \
        Rscript \
        "$G4_IMGRINDER" \
        "$JOB_FASTA" \
        "$OUTFILE"

    rm "$JOB_FASTA"
done
