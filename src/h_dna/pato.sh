#!/bin/bash
#SBATCH --job-name=pato
#SBATCH --array=1-5
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --partition=gpu-a100
#SBATCH --account=MCB26029
#SBATCH --output=logs/h_dna/pato/run_%a.out
#SBATCH --error=logs/h_dna/pato/run_%a.err

set -euo pipefail
export OMP_NUM_THREADS=1

RUN=${SLURM_ARRAY_TASK_ID}

FASTA="data/chr18.fa"
OUTDIR="results/h_dna/pato/run_${RUN}"
OUTFILE="$OUTDIR/res.bed"
BENCH="benchmarks/h_dna/pato/run_${RUN}.txt"
PATO="src/h_dna/dependencies/pato/build/tools/PATO/PATO"

mkdir -p "$OUTDIR" "$(dirname "$BENCH")"

JOB_FASTA="${OUTDIR}/clean_chr18.fa"
cp "$FASTA" "$JOB_FASTA"

/usr/bin/time -v -o "$BENCH" \
    "$PATO" \
    --duplex-file "$JOB_FASTA" \
    --output "$OUTFILE"

rm "$JOB_FASTA"
