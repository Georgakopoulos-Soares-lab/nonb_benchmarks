# Inverted repeats (IR)

This category covers tools that detect inverted repeats and hairpin/cruciform structures.

Cloned or downloaded tools go in `src/ir/dependencies/` (git-ignored). Run the
install commands below from that directory:

```
mkdir -p src/ir/dependencies
cd src/ir/dependencies
```

## Tools

### IRF (Inverted Repeats Finder)

https://github.com/Benson-Genomics-Lab/IRF

```
git clone https://github.com/Benson-Genomics-Lab/IRF
cd IRF/src
make
```

Binary: `dependencies/IRF/bin/irf.exe`.
Script: `irf.sh`, which runs `irf.exe <fasta> 2 3 5 80 10 20 10000 101 -h -d`.

### GRF (GenericRepeatFinder)

https://github.com/bioinfolabmu/GenericRepeatFinder

```
git clone https://github.com/bioinfolabmu/GenericRepeatFinder
cd GenericRepeatFinder/src
make
```

Binary: `dependencies/GenericRepeatFinder/bin/grf-main`. The repo also ships
prebuilt binaries in `bin/`.
Script: `grf.sh`. It runs `grf-main -c 0 -t 1 -f 0 --min_tr 10 --max_tr 450 --min_spacer_len 0
--max_spacer_len 100 --max_indel 0 --max_mismatch 0 --seed_mismatch 0`.

### IUPACpal

```
git clone https://github.com/steven31415/IUPACpal
cd IUPACpal
export CMAKE_POLICY_VERSION_MINIMUM=3.5
./pre-install.sh
make -f Makefile.gcc
```

Binary: `dependencies/IUPACpal/IUPACpal`.
Script: `iupacpal.sh`, which runs `IUPACpal -s NC_060942.1 -m 10 -M 450 -g 100 -x 0`.

### NeSSie

```
git clone https://github.com/B3rse/nessie
cd nessie
make
```

Binary: `dependencies/nessie/nessie`.
Script: `nessie.sh`, which runs `nessie --palindrome --kmin 20 --kmax 900 --MAX`. NeSSie takes a long
time on chr18. `missing_jobs.sh` runs the same loop under SBATCH headers
(edit `--partition`/`--account` first) and is submitted with
`sbatch src/ir/missing_jobs.sh [NRUNS]`.

### Einverted (EMBOSS)

```
conda install -c conda-forge -c bioconda emboss
```

Script: `einverted.sh`. It runs `einverted -gap 12 -threshold 30 -match 3 -mismatch -4
-maxrepeat 1000 -outfile res.einverted -outseq res.inv.fa`.

### detectIR (MATLAB)

Download `detectIR.20150213.7z` from https://sourceforge.net/projects/detectir/
and extract it into `dependencies/detectIR/`:

```
mkdir detectIR && cd detectIR
7z x ../detectIR.20150213.7z && rm ../detectIR.20150213.7z
```

Script: `detectIR.sh`. It runs `module load matlab` and then `src/ir/detectIR.m`, which calls
`detectPerfectIR(seq, 10, 1000)` and `detectImperfectIR(seq, 20, 1000, 6)` and
writes FASTA and runtime files for each.

### FindIR (MATLAB)

The code comes from the supplementary material of
https://academic.oup.com/bioinformatics/article/30/6/887/287234. Extract it into
`dependencies/findIR/` so that `dependencies/findIR/findIR.m` exists.

Script: `findIR.sh`. It runs `module load matlab` and then `src/ir/findIR.m`, which calls
`findIR(inputFile, 4, 1000)`.

Both MATLAB scripts get their input and output paths from environment variables
(`IR_FUNCDIR`, `IR_INPUT`, ...). The `.sh` script exports them and the `.m`
script reads them with `getenv()`.

### Non-B GFA (IR mode)

Build non-B GFA once under `src/general/` (see
[src/general/README.md](../general/README.md)).

Script: `gfa.sh`, which runs `gfa -seq <fasta> -out gfa_out -minIRrep 10 -maxIRspacer 100` with
every structure type except IRs skipped.

## Running the benchmarks

Run from the repository root with the `nonb-tools` env active. `NRUNS` is
optional and defaults to 1:

```
bash src/ir/<tool>.sh [NRUNS]
```

Output goes to `results/ir/<Tool>/run_<N>/` and the `/usr/bin/time -v` report to
`benchmarks/ir/<Tool>/run_<N>.txt`. `<Tool>` is one of `IRF`, `GRF`,
`IUPACpal`, `NeSSie`, `Einverted`, `DetectIR`, `FindIR`, `Non-B GFA IR`.