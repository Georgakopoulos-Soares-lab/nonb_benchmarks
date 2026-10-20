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
    OUTDIR="$ROOT/results/g4/G4mismatch/run_${RUN}"
    BENCH="$ROOT/benchmarks/g4/G4mismatch/run_${RUN}.txt"
    G4MISMATCH="$ROOT/src/g4/dependencies/G4mismatch/G4mismatch_scan.py"
    MODEL="$ROOT/src/g4/dependencies/G4mismatch/models/model_KPDS.h5"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="$OUTDIR/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    ulimit -c unlimited

    cd "$OUTDIR"

    /usr/bin/time -v -o "$BENCH" \
        python "$G4MISMATCH" \
            --data_path "$JOB_FASTA" \
            --model_path "$MODEL" \
            --out_file "$OUTDIR" \
            --merge 1 \
            --reverse_complement 1 \
            --filter_bins 14.4 \
            --multiprocessing 0 \
            --batch_size 128

    rm "$JOB_FASTA"

done