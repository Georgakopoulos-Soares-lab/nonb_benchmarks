# G-quadruplexes (G4)

Tools benchmarked here detect G-quadruplex (G4) forming sequences.

## Tools

### pqsfinder

Bioconductor R package.

```
conda install -y -c conda-forge -c bioconda bioconductor-pqsfinder bioconductor-rtracklayer bioconductor-genomicranges
```

Run: `sbatch src/g4/pqsfinder.sh`. Calls the wrapper `src/g4/pqsfinder.R`
(`pqsfinder()` on the input FASTA), which writes a BED file.

### G4Hunter

Python 3 port, from https://github.com/Georgakopoulos-Soares-lab/G4Hunter-Companion

```
git clone https://github.com/Georgakopoulos-Soares-lab/G4Hunter-Companion
cd G4Hunter-Companion
conda install -c conda-forge -c bioconda datrie==0.8.2 pybedtools==0.12.0 bedtools
python -m pip install -e .
```

Run: `sbatch src/g4/g4hunter.sh`. Invokes `g4hunter --outdir <dir> <fasta>`.

### Quadron

From https://github.com/aleksahak/Quadron

```
install.packages(c("plyr", "data.table", "caret", "shiny", "doMC", "foreach", "itertools"))

git clone https://github.com/aleksahak/Quadron   # large repo, clone takes a while

install.packages(
    "http://cran.r-project.org/src/contrib/Archive/xgboost/xgboost_0.4-4.tar.gz",
    repos = NULL,
    type = "source"
)

cd Quadron/lib
# in R:
source("bitcompile.R")
```

Expected at `src/g4/dependencies/Quadron/Quadron.lib`.

Run: `sbatch src/g4/quadron.sh` (GPU partition). Calls the wrapper
`src/g4/quadron.R`, which loads `Quadron.lib` and runs
`Quadron(FastaFile=..., OutFile=..., nCPU=1, SeqPartitionBy=1000000)`.

### G4Boost

Requires Python 3.9 specifically — more recent Python builds break the pinned
dependencies. From https://github.com/hbusra/G4Boost

```
git clone https://github.com/hbusra/G4Boost.git
cd G4Boost
conda create -p g4boost -c conda-forge python=3.9 numpy=1.23 pandas=1.4.3 scikit-learn=1.0.2 py-xgboost=1.4.2
```

Expected at `src/g4/dependencies/G4Boost/G4Boost_v4.py`.

Run: `sbatch src/g4/g4boost.sh` (GPU partition). Invokes
`python3 G4Boost_v4.py --fasta <fasta> -g 3`.

### G4detector

From https://github.com/OrensteinLab/G4detector

```
git clone https://github.com/OrensteinLab/G4detector
```

Requires Keras 2.1.6 with the TensorFlow backend. Vendored under
`src/g4/dependencies/G4detector`; not yet wired up to a benchmark script.

## Running the benchmarks

Submit `sbatch src/g4/<tool>.sh` from the repository root (`pqsfinder`, `g4hunter`,
`quadron`, `g4boost`). Each script is a 5-task job array that runs the tool once
on `data/chr18.fa` per task, timed with `/usr/bin/time -v`. Output goes to
`results/g4/<tool>/run_<N>/`, timing to `benchmarks/g4/<tool>/run_<N>.txt`, and
SLURM logs to `logs/g4/<tool>/run_<N>.{out,err}`. `quadron` and `g4boost` are
submitted to a GPU partition; the others to CPU.


QGRS Mapper
git clone https://github.com/freezer333/qgrs-cpp

cd qgrs-cpp
g++ -o qgrs src/default.cpp src/qgrs.cpp --std=c++11

G4-iM Grinder (Installation takes a while)
pck <- c(
  "stringr", "stringi", "plyr", "seqinr", "stats", "parallel", 
  "doParallel", "beepr", "stats4", "devtools", "dplyr", 
  "BiocManager", "tibble"
)

foo <- function(x){
  for( i in x ){
    if( ! require( i , character.only = TRUE ) ){
      install.packages( i , dependencies = TRUE )
      require( i , character.only = TRUE )
    }
  }
}

foo(pck)

BiocManager::install(c("BiocGenerics", "S4Vectors", "Biostrings", "biomartr", "IRanges"), 
                     ask = FALSE, update = TRUE)

maybe if the above returns errors on some libraries

conda install -c conda-forge -c bioconda \
  r-xml2 r-xml r-rcurl r-biocmanager \
  bioconductor-biomart r-biomartr

conda install -c conda-forge r-systemfonts r-textshaping r-ragg r-pkgdown r-devtools
devtools::install_github("EfresBR/G4iMGrinder")

library(G4iMGrinder)

G4Catchall
git clone https://github.com/odoluca/G4Catchall

QPARSE
install numpy 
git clone https://github.com/B3rse/qparse

ImGQfinder
git clone https://github.com/PollyTikhonova/ImGQfinder
cd ImGQfinder
python -m pip install -r requirements.txt
