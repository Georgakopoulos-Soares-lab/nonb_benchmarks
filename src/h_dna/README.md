# H-DNA / triplexes

Tools benchmarked here detect triplex-forming sequences (H-DNA).

## Tools

### triplex (Bioconductor)

```
conda install -y bioconductor-rtracklayer bioconductor-genomicranges

if (!require("BiocManager", quietly = TRUE)) {
    install.packages("BiocManager")
}

BiocManager::install("triplex")
```

Run: `sbatch src/h_dna/triplex.sh`. Calls the wrapper `src/h_dna/triplex.R`
(`triplex.search()` on the input FASTA), which writes a BED file.

### Hseeker

```
pip install hseeker
```

Run: `sbatch src/h_dna/hseeker.sh`. Invokes
`hseeker -seq <fasta> -out <prefix> -workers 1`.

### TriplexFPP

From https://github.com/yuuuuzhang/TriplexFPP

```
git clone https://github.com/yuuuuzhang/TriplexFPP
conda install -c conda-forge numpy pandas biopython
pip install "tensorflow[and-cuda]"
```

Expected under `src/h_dna/dependencies/TriplexFPP/code` (must contain
`triplex_util.py`).

Run: `sbatch src/h_dna/triplexfpp.sh` (GPU partition). Calls the wrapper
`src/h_dna/triplexfpp.py`, which imports `triplex_util.triplex_DNA` and runs it
against the FASTA.

### triplexator

From https://github.com/Gurado/triplexator

```
git clone https://github.com/Gurado/triplexator
cd triplexator
mkdir -p build/Release && cd build/Release

sed -i '933s/^/\/\//' src/seqan/file/file_generated_forwards.h
sed -i 's/::std::make_pair<unsigned,::std::pair< ::std::string,unsigned> >(seqNo,::std::make_pair< ::std::string,unsigned>(filename,seqNoWithinFile))/::std::make_pair(seqNo,::std::make_pair(filename,seqNoWithinFile))/g' src/triplexator.cpp

cmake ../.. -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=g++ \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DBoost_NO_BOOST_CMAKE=ON \
    -DCMAKE_DISABLE_FIND_PACKAGE_Boost=ON -G "Unix Makefiles" && make
cd ../..
./bin/triplexator --help
```

The `sed` patches work around a SeqAN/Boost compatibility issue when building
with a modern compiler/CMake. Expected at
`src/h_dna/dependencies/triplexator/bin/triplexator`.

Run: `sbatch src/h_dna/triplexator.sh` (GPU partition). Invokes
`triplexator --duplex-file <fasta> --output res.bed --output-format 0
--runtime-mode 0 --processors 1`.

## Running the benchmarks

Submit `sbatch src/h_dna/<tool>.sh` from the repository root (`triplex`,
`hseeker`, `triplexfpp`, `triplexator`). Each script is a 5-task job array that
runs the tool once on `data/chr18.fa` per task, timed with `/usr/bin/time -v`.
Output goes to `results/h_dna/<tool>/run_<N>/`, timing to
`benchmarks/h_dna/<tool>/run_<N>.txt`, and SLURM logs to
`logs/h_dna/<tool>/run_<N>.{out,err}`. `triplexfpp` and `triplexator` are
submitted to a GPU partition; `triplex` and `hseeker` to CPU.


PATO

git clone https://github.com/UDC-GAC/pato

cd pato
cmake -B build . && cmake --build build

 ./build/tools/PATO/PATO 