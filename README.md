# Benchmarking of non-B DNA detection algorithms

Benchmarking suite for non-B DNA structure detection algorithms. Each tool is run
on chromosome 18 of the T2T-CHM13v2.0 human genome assembly and timed with
`/usr/bin/time -v`, so runtime and peak memory can be compared across methods.
The predicted structures are then compared across tools within each category.

## Structure categories and tools

Each non-B DNA structure family has its own directory under `src/`. Each one has
a README with that category's install steps and run instructions:

| Category | Structure | Tools | README |
|---|---|---|---|
| `dr_and_str` | Direct repeats / short tandem repeats | Dot2dot, Etandem, Mreps, Non-B GFA STR, PERF, Pytrf, TRF, ULTRA | [src/dr_and_str/README.md](src/dr_and_str/README.md) |
| `g4` | G-quadruplexes | G4Boost, G4Catchall, G4Hunter, G4-iM Grinder, G4mismatch, G4predict, ImGQfinder, Non-B GFA G4, Pqsfinder, QGRS Mapper, QPARSE, Quadparser, Quadron | [src/g4/README.md](src/g4/README.md) |
| `h_dna` | H-DNA / triplexes | HSeeker, Triplex | [src/h_dna/README.md](src/h_dna/README.md) |
| `ir` | Inverted repeats / hairpins | DetectIR, Einverted, FindIR, GRF, IRF, IUPACpal, NeSSie, Non-B GFA IR | [src/ir/README.md](src/ir/README.md) |
| `r_loops` | R-loops | DeepER, deepRloopPre, QmRLFS-finder | [src/r_loops/README.md](src/r_loops/README.md) |
| `z_dna` | Z-DNA | Non-B GFA Z-DNA, ZDNABERT, Z-Hunt, ZSeeker | [src/z_dna/README.md](src/z_dna/README.md) |

[src/general/](src/general/README.md) holds non-B GFA, which is shared across
categories: its G4, Z-DNA, STR and IR modes are each benchmarked in the matching
category.

## Repository layout

```
data/              reference FASTA (downloaded, not checked in)
src/<cat>/         one run script per tool (<tool>.sh, plus R/Python/MATLAB
                   wrappers where needed) and dependencies/ (cloned and built
                   tool source, not checked in)
src/general/       shared tools (non-B GFA)
src/comparisons/   runtime/memory plot and per-category overlap plots
src/download_data.sh
results/           tool output, one directory per run; results/plots/ for figures
benchmarks/        `/usr/bin/time -v` output for each run
logs/              SLURM stdout/stderr for long jobs submitted with sbatch
```

`data/`, `results/`, `benchmarks/`, `logs/` and every `dependencies/` directory
are git-ignored.

Output paths follow one pattern, where `<Tool>` is the tool's display name
(e.g. `G4Hunter`, `Non-B GFA Z-DNA`) and `<N>` is the run number:

```
results/<cat>/<Tool>/run_<N>/
benchmarks/<cat>/<Tool>/run_<N>.txt
```

## Setup

```
conda activate nonb-tools   # python 3.10
```

Each tool also needs its own dependencies (R packages, other conda envs,
compiled binaries, MATLAB, Python packages). The category READMEs linked above
list them.

Download the reference data (T2T-CHM13v2.0 from NCBI) and extract chromosome 18
(`NC_060942.1`) to `data/chr18.fa`. The script uses a relative path, so run it
from `src/`:

```
cd src
bash download_data.sh
cd ..
```

This requires `wget` and `samtools`.

## Running a benchmark

From the repository root, run the script for a tool, optionally giving the
number of runs (default 1):

```
bash src/z_dna/zseeker.sh        # one run
bash src/g4/g4hunter.sh 5        # five runs: run_1 .. run_5
```

For each run, the script copies `data/chr18.fa` into the run's results directory
and runs the tool on that copy under `/usr/bin/time -v`. It then deletes the copy.

Scripts must be launched from the repository root because they resolve every path
against `$(pwd)`.

## Comparisons and plots

The scripts in `src/comparisons/` read from `results/` and `benchmarks/` and
write PDFs to `results/plots/`. They use paths relative to their own directory,
so run them from there:

```
cd src/comparisons
python benchmark_plot.py     # runtime (user time) and peak memory for all tools
python g4_upset.py           # G4 overlap (UpSet)
python z_dna_venn.py         # Z-DNA overlap (Venn)
python ir_venn.py            # IR overlap (Venn)
python dr_and_str_venn.py    # DR/STR overlap (Venn)
python h_dna_euler.py        # H-DNA overlap (Euler)
```
