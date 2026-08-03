# Benchmarking of non-B DNA detection algorithms

Benchmarking suite for non-B DNA structure detection algorithms. Each tool is run
on chromosome 18 of the T2T-CHM13v2.0 human genome assembly and timed with
`/usr/bin/time -v` so that runtime and peak memory can be compared across methods.

## Structure categories

Each non-B DNA structure family lives in its own directory under `src/`, with its
own README covering the specific tools, install steps, and run instructions:

| Category | Structure | README |
|---|---|---|
| `dr_and_str` | Direct repeats / short tandem repeats | [src/dr_and_str/README.md](src/dr_and_str/README.md) |
| `g4` | G-quadruplexes | [src/g4/README.md](src/g4/README.md) |
| `general` | General repeat finders (TIRs, EMBOSS tools, non-B GFA) | [src/general/README.md](src/general/README.md) |
| `h_dna` | H-DNA / triplexes | [src/h_dna/README.md](src/h_dna/README.md) |
| `ir` | Inverted repeats / hairpins | [src/ir/README.md](src/ir/README.md) |
| `r_loops` | R-loops | [src/r_loops/README.md](src/r_loops/README.md) |
| `z_dna` | Z-DNA | [src/z_dna/README.md](src/z_dna/README.md) |

## Repository layout

```
data/         reference FASTA(s) used for benchmarking (downloaded, not checked in)
src/<cat>/    sbatch scripts + wrapper scripts for each tool, plus dependencies/
              (vendored/cloned tool source, built locally)
results/      per-run tool output (BED/TSV/FASTA/etc.), one dir per run
benchmarks/   per-run `/usr/bin/time -v` output (wall clock, peak RSS, ...)
logs/         per-run SLURM stdout/stderr
src/plots.ipynb  aggregates results/benchmarks into results/plots/
```

Within a category, results/benchmarks/logs follow the same pattern:
`results/<cat>/<tool>/run_<N>/`, `benchmarks/<cat>/<tool>/run_<N>.txt`,
`logs/<cat>/<tool>/run_<N>.{out,err}`, where `<N>` is the SLURM array task ID.

## Setup

```
conda activate nonb-tools   # python 3.10
```

Each tool has its own additional dependencies (R packages, other conda envs,
compiled binaries, Python packages). See the category READMEs linked above.

Download and prepare the reference data (T2T-CHM13v2.0, chromosome 18 only):

```
bash src/download_data.sh
```

## Reproducing a benchmark

From the repository root, submit the sbatch script for the tool you want to run,
e.g.:

```
sbatch src/z_dna/zseeker.sh
```

Each script is a SLURM job array (`run_1` .. `run_5`) that runs the tool once per
array task on `data/chr18.fa`, wrapped in `/usr/bin/time -v` for timing.

The `--partition` and `--account` values in the SBATCH headers are specific to
the cluster this was developed on (TACC) — edit them for your own allocation
before submitting.