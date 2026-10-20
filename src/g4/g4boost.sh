#!/bin/bash

set -euo pipefail

NRUNS=${1:-1}

if ! [[ "$NRUNS" =~ ^[1-9][0-9]*$ ]]; then
    echo "Usage: $0 [NRUNS]  (NRUNS must be a positive integer)" >&2
    exit 1
fi

ROOT="$(pwd)"

FASTA="$ROOT/data/chr18.fa"
G4BOOST_DIR="$ROOT/src/g4/dependencies/G4Boost"
G4BOOST="$G4BOOST_DIR/G4Boost.py"
G4BOOST_CLASSIFIER="$G4BOOST_DIR/G4Boost_classifier.json"
G4BOOST_REGRESSOR="$G4BOOST_DIR/G4Boost_regressor.json"

for RUN in $(seq 1 "$NRUNS"); do

    OUTDIR="$ROOT/results/g4/g4boost/run_${RUN}"
    BENCH="$ROOT/benchmarks/g4/g4boost/run_${RUN}.txt"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"
    cp "$FASTA" "$JOB_FASTA"

    (
        cd "$OUTDIR"
        /usr/bin/time -v -o "$BENCH" \
            python3 "$G4BOOST" \
            --fasta "$JOB_FASTA" \
            -g 3 \
            -G 4 \
            -n 1 \
            -N 9 \
            -l 11 \
            --classifier "$G4BOOST_CLASSIFIER" \
            --regressor "$G4BOOST_REGRESSOR"
    )

    rm "$JOB_FASTA"
done