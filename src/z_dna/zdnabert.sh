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
    OUTDIR="$ROOT/results/z_dna/zdnabert/run_${RUN}"
    OUTFILE="$OUTDIR/res.txt"
    BENCH="$ROOT/benchmarks/z_dna/zdnabert/run_${RUN}.txt"
    ZDNABERT="$ROOT/src/z_dna/zdnabert.py"

    DEPENDENCY_DIR="$ROOT/src/z_dna/dependencies"
    JOB_MODEL_DIR="${OUTDIR}/model_bin"

    mkdir -p "$OUTDIR" "$(dirname "$BENCH")" "$JOB_MODEL_DIR"

    JOB_FASTA="${OUTDIR}/clean_chr18.fa"

    cp "$FASTA" "$JOB_FASTA"

    cp "$DEPENDENCY_DIR/Z-DNABERT/config.json" \
        "$DEPENDENCY_DIR/Z-DNABERT/special_tokens_map.json" \
        "$DEPENDENCY_DIR/Z-DNABERT/tokenizer_config.json" \
        "$DEPENDENCY_DIR/Z-DNABERT/vocab.txt" \
        "$DEPENDENCY_DIR/Z-DNABERT/models/HG_kouzine/pytorch_model.bin" \
        "$JOB_MODEL_DIR"

    /usr/bin/time -v -o "$BENCH" \
        python \
        "$ZDNABERT" \
        "$JOB_MODEL_DIR" \
        "$JOB_FASTA" \
        "$OUTFILE"

    rm "$JOB_FASTA"
done