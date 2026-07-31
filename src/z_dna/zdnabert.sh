#!/bin/bash
#SBATCH --job-name=zdnabert
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/z_dna/zdnabert/run_%a.out
#SBATCH --error=logs/z_dna/zdnabert/run_%a.err

set -euo pipefail

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/z_dna/zdnabert/run_${RUN}"
OUTFILE="$OUTDIR/res.txt"
BENCH="benchmarks/z_dna/zdnabert/run_${RUN}.txt"
ZDNABERT="src/z_dna/zdnabert.py"

DEPENDENCY_DIR="src/z_dna/dependencies"
JOB_MODEL_DIR="${OUTDIR}/model_bin"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")" "$JOB_MODEL_DIR"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"

cp "$FASTA" "$JOB_FASTA"

cp "$DEPENDENCY_DIR/Z-DNABERT/config.json" \
    "$DEPENDENCY_DIR/Z-DNABERT/special_tokens_map.json" \
    "$DEPENDENCY_DIR/Z-DNABERT/tokenizer_config.json" \
    "$DEPENDENCY_DIR/Z-DNABERT/vocab.txt" \
    "$DEPENDENCY_DIR/Z-DNABERT/models/HG_chipseq/pytorch_model.bin" \
    "$JOB_MODEL_DIR"

/usr/bin/time -v -o "$BENCH" \
    python \
    "$ZDNABERT" \
    "$JOB_MODEL_DIR" \
    "$JOB_FASTA" \
    "$OUTFILE"

rm "$JOB_FASTA"
