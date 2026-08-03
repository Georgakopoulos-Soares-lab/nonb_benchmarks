# Inverted repeats (IR)

Tools benchmarked here detect inverted repeats / hairpin structures.

## Tools

### IRF (Inverted Repeats Finder)

From https://github.com/Benson-Genomics-Lab/IRF

```
git clone https://github.com/Benson-Genomics-Lab/IRF
cd IRF/src
make
cd ..
```

Expected at `src/ir/dependencies/IRF/bin/irf.exe`.

Run: `sbatch src/ir/irf.sh`. Invokes
`irf.exe <fasta> 2 3 5 80 10 20 100000 1000000 -h -d`.

### detectIR

From https://sourceforge.net/projects/detectir/

```
7z x detectIR.20150213.7z && rm detectIR.20150213.7z
```

MATLAB functions for detecting both perfect and imperfect inverted repeats.
Expected under `src/ir/dependencies/detectIR`.

Run: `sbatch src/ir/detectIR.sh` (loads the cluster's `matlab` module). Runs
`src/ir/detectIR.m`, which calls `detectPerfectIR(seq, 10, 1000)` and
`detectImperfectIR(seq, 20, 1000, 6)` and writes FASTA + runtime files for each.

### matlabIR

Supplementary material from
https://academic.oup.com/bioinformatics/article/30/6/887/287234

Expected under `src/ir/dependencies/MATLAB_IR`.

Run: `sbatch src/ir/matlabIR.sh` (loads the cluster's `matlab` module). Runs
`src/ir/matlabIR.m`, which calls `findIR(inputFile, 4, 1000)`.

## Running the benchmarks

Submit `sbatch src/ir/<irf|detectIR|matlabIR>.sh` from the repository root.
Each script is a 5-task job array that runs the tool once on `data/chr18.fa`
per task, timed with `/usr/bin/time -v`. Output goes to
`results/ir/<tool>/run_<N>/`, timing to `benchmarks/ir/<tool>/run_<N>.txt`, and
SLURM logs to `logs/ir/<tool>/run_<N>.{out,err}` (tool names are lowercased in
the log/results paths: `detectir`, `matlabir`). The MATLAB-based tools
(`detectIR`, `matlabIR`) pass the input/output paths via environment
variables set in the sbatch script, read by the `.m` scripts with `getenv()`.
