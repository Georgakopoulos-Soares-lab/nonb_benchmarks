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
    OUTDIR="$ROOT/results/g4/G4Catchall/run_${RUN}"
    OUTFILE="$OUTDIR/res.txt"
    BENCH="$ROOT/benchmarks/g4/G4Catchall/run_${RUN}.txt"
    G4CATCHALL="$ROOT/src/g4/dependencies/G4Catchall/G4Catchall.py"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"
    
    ulimit -c unlimited
    cd "$OUTDIR"
    
    (
        /usr/bin/time -v -o "$BENCH" \
            python \
            "$G4CATCHALL" \
            --fasta "$JOB_FASTA" \
            --G3GQ_loop 1..9 \
            --max_imperfect_Gtracts 0 > $OUTFILE
    )

    rm "$JOB_FASTA"
done