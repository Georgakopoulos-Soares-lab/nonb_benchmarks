# G-quadruplexes (G4)

This category covers tools that detect G-quadruplex (G4) forming sequences. Where the tool
exposes them, the parameters are set to canonical G4s: G-runs of 3–4 nt, 4 runs,
loops of 1–9 nt and no bulges.

Cloned tools go in `src/g4/dependencies/` (git-ignored). Run the clone commands
below from that directory:

```
mkdir -p src/g4/dependencies
cd src/g4/dependencies
```

## Tools

### pqsfinder

This is a Bioconductor R package, so there is nothing to clone.

```
conda install -c conda-forge -c bioconda bioconductor-pqsfinder bioconductor-rtracklayer bioconductor-genomicranges
```

Script: `pqsfinder.sh`. It calls `src/g4/pqsfinder.R`, which runs
`pqsfinder(seq, max_bulges=0, run_min_len=3, run_max_len=4, loop_min_len=1, loop_max_len=9)`
and writes `res.bed`.

### G4Hunter and Quadparser

Both tools come from the G4Hunter-Companion package
(https://github.com/Georgakopoulos-Soares-lab/G4Hunter-Companion):

```
git clone https://github.com/Georgakopoulos-Soares-lab/G4Hunter-Companion
cd G4Hunter-Companion
conda install -c conda-forge -c bioconda datrie==0.8.2 pybedtools==0.12.0 bedtools
python -m pip install -e .
```

Scripts:
- `g4hunter.sh` runs `g4hunter --window-size 25 --min_score 1.5 --min-loop-length 1 --max-loop-length 9`.
- `quadparser.sh` runs the same command with `--parse-consensus` added, which gives the
  Quadparser regex search.

### Quadron

https://github.com/aleksahak/Quadron. The repo is large, so the clone takes a
while.

```
conda install -c conda-forge zlib
git clone https://github.com/aleksahak/Quadron
```

In R:

```
install.packages(c("plyr", "data.table", "caret", "shiny", "doMC", "foreach", "itertools"))
install.packages(
    "http://cran.r-project.org/src/contrib/Archive/xgboost/xgboost_0.4-4.tar.gz",
    repos = NULL, type = "source"
)
setwd("Quadron/lib")
source("bitcompile.R")      # builds Quadron/Quadron.lib
```

Library: `dependencies/Quadron/Quadron.lib`.
Script: `quadron.sh`. It calls `src/g4/quadron.R`, which loads the library and runs
`Quadron(FastaFile, OutFile, nCPU = 1)`.

### G4Boost

https://github.com/hbusra/G4Boost. It needs Python 3.9, because newer versions
break the pinned dependencies. Use a separate env and activate it before running
the script.

```
git clone https://github.com/hbusra/G4Boost
conda create -n g4boost -c conda-forge python=3.9 numpy=1.23 pandas=1.4.3 scikit-learn=1.0.2 py-xgboost=1.4.2
```

The script uses `dependencies/G4Boost/G4Boost.py` with the
`G4Boost_classifier.json` and `G4Boost_regressor.json` models that come with the repo.
Script: `g4boost.sh`, which runs `G4Boost.py -g 3 -G 4 -n 1 -N 9 -l 11`.

### QGRS Mapper

C++ port: https://github.com/freezer333/qgrs-cpp

```
git clone https://github.com/freezer333/qgrs-cpp
cd qgrs-cpp
g++ -o qgrs src/default.cpp src/qgrs.cpp --std=c++11
```

Binary: `dependencies/qgrs-cpp/qgrs`.
Script: `qgrs_mapper.sh`, which runs `qgrs -csv -t 3`.

### G4-iM Grinder

https://github.com/EfresBR/G4iMGrinder. This R package takes a while to install.

```
conda install -c conda-forge r-systemfonts r-textshaping r-ragg r-pkgdown r-devtools
```

In R:

```
pck <- c("stringr", "stringi", "plyr", "seqinr", "stats", "parallel",
         "doParallel", "beepr", "stats4", "devtools", "dplyr",
         "BiocManager", "tibble")
for (p in pck) {
  if (!require(p, character.only = TRUE)) {
    install.packages(p, dependencies = TRUE)
  }
}

BiocManager::install(c("BiocGenerics", "S4Vectors", "Biostrings", "biomartr", "IRanges"),
                     ask = FALSE, update = TRUE)

devtools::install_github("EfresBR/G4iMGrinder")
```

If any of the Bioconductor or biomartr installs fail, install these from conda and
then retry:

```
conda install -c conda-forge -c bioconda r-xml2 r-xml r-rcurl r-biocmanager bioconductor-biomart r-biomartr
```

Script: `g4_imgrinder.sh`. It calls `src/g4/g4_imgrinder.R`, which runs
`G4iMGrinder(BulgeSize=0, MinRunSize=3, MaxRunSize=4, MinLoopSize=1, MaxLoopSize=9, MinNRuns=4, MaxNRuns=4)`
and writes `res.csv`.

### G4Catchall

```
git clone https://github.com/odoluca/G4Catchall
pip install regex
```

Script: `g4catchall.sh`. It runs `dependencies/G4Catchall/G4Catchall.py` with
`--G3GQ_loop 1..9 --max_imperfect_Gtracts 0` and redirects stdout to `res.txt`.

### QPARSE

```
git clone https://github.com/B3rse/qparse
pip install "numpy<1.24"
```

Script: `qparse.sh`. It runs `dependencies/qparse/QPARSE_1.10.py` with
`--minlen 3 --maxlen 4 --maxloop 9`.

### ImGQfinder

```
git clone https://github.com/PollyTikhonova/ImGQfinder
cd ImGQfinder
python -m pip install -r requirements.txt "numpy==1.23.5"
```

Script: `imgqfinder.sh`. It runs `dependencies/ImGQfinder/imgqfinder.py` with
`-L 9 -mdef 0 -maxbulge 0 -tetdef 0 --nthreads 1 --repeats --output_type 1`.

### G4predict

```
git clone https://github.com/mparker2/g4predict
cd g4predict
python setup.py build
python setup.py install
```

Script: `g4predict.sh`, which runs `g4predict intra --min-tetrad 3 --max-tetrad 4 --min-loop 1
--max-loop 9 --bulges 0`.

### G4mismatch

https://github.com/OrensteinLab/G4mismatch. It needs Python 3.9–3.11.

```
git clone https://github.com/OrensteinLab/G4mismatch
python -m pip install "tensorflow[and-cuda]==2.15.1" "numpy<2" "pandas<2" biopython joblib
```

Script: `g4mismatch.sh`. It runs `dependencies/G4mismatch/G4mismatch_scan.py` with
the `models/model_KPDS.h5` model that comes with the repo, plus `--merge 1 --reverse_complement 1
--filter_bins 14.4 --multiprocessing 0 --batch_size 128`.

### Non-B GFA (G4 mode)

Build non-B GFA once under `src/general/` (see
[src/general/README.md](../general/README.md)).

Script: `gfa.sh`, which runs `gfa -seq <fasta> -out gfa_out -minGQrep 3 -maxGQspacer 9` with
every structure type except G4s skipped.

## Running the benchmarks

Run from the repository root with the right env active: `nonb-tools` for most
tools, and the `g4boost` env for G4Boost. `NRUNS` is optional and defaults to 1:

```
bash src/g4/<tool>.sh [NRUNS]
```

Output goes to `results/g4/<Tool>/run_<N>/` and the `/usr/bin/time -v` report to
`benchmarks/g4/<Tool>/run_<N>.txt`. `<Tool>` is one of `Pqsfinder`, `G4Hunter`,
`Quadparser`, `Quadron`, `G4Boost`, `QGRS Mapper`, `G4-iM Grinder`,
`G4Catchall`, `QPARSE`, `ImGQfinder`, `G4predict`, `G4mismatch`,
`Non-B GFA G4`.
