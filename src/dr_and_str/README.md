# Direct repeats & short tandem repeats

Tools benchmarked here detect direct repeats and short tandem repeats (STRs).

## Tools

### TRF (Tandem Repeats Finder)

From https://github.com/Benson-Genomics-Lab/TRF

```
git clone https://github.com/Benson-Genomics-Lab/TRF
cd TRF/
mkdir build && cd build
../configure
make
```

Expected at `src/dr_and_str/dependencies/TRF/build/src/trf`.

Run: `sbatch src/dr_and_str/trf.sh`. Invokes
`trf <fasta> 2 7 7 80 10 50 500 -f -d -m -h`.

### mreps

From https://github.com/gregorykucherov/mreps

```
git clone https://github.com/gregorykucherov/mreps.git
cd mreps
make
```

Expected at `src/dr_and_str/dependencies/mreps/mreps`.

Run: `sbatch src/dr_and_str/mreps.sh`. Invokes
`mreps -fasta -xmloutput res.xml <fasta>`.

## Running the benchmarks

Submit `sbatch src/dr_and_str/<trf|mreps>.sh` from the repository root. Each
script is a 5-task job array that runs the tool once on `data/chr18.fa` per
task, timed with `/usr/bin/time -v`. Output goes to
`results/dr_and_str/<tool>/run_<N>/`, timing to
`benchmarks/dr_and_str/<tool>/run_<N>.txt`, and SLURM logs to
`logs/dr_and_str/<tool>/run_<N>.{out,err}`.

ULTRA
git clone https://github.com/TravisWheelerLab/ULTRA
cd ULTRA
cmake .
make

Dot2dot
git clone https://github.com/Gege7177/Dot2dot

Pytrf
pip install -U pytrf

PERF
pip install perf_ssr