# Direct repeats & short tandem repeats

This category covers tools that detect direct repeats and short tandem repeats (STRs). All
tools are run with motif sizes of 1–6 bp and a minimum repeat length of 12 bp
wherever the tool exposes those parameters.

Cloned or built tools go in `src/dr_and_str/dependencies/` (git-ignored). Run the
install commands below from that directory:

```
mkdir -p src/dr_and_str/dependencies
cd src/dr_and_str/dependencies
```

## Tools

### TRF (Tandem Repeats Finder)

https://github.com/Benson-Genomics-Lab/TRF

```
git clone https://github.com/Benson-Genomics-Lab/TRF
cd TRF
mkdir build && cd build
../configure
make
```

Binary: `dependencies/TRF/build/src/trf`.
Script: `trf.sh`, which runs `trf <fasta> 2 7 7 80 10 24 6 -f -h -d -m`.

### mreps

https://github.com/gregorykucherov/mreps

```
git clone https://github.com/gregorykucherov/mreps
cd mreps
make
```

Binary: `dependencies/mreps/mreps`.
Script: `mreps.sh`, which runs `mreps -fasta -xmloutput res.xml -minperiod 1 -maxperiod 6 -minsize 12 <fasta>`.

### ULTRA

https://github.com/TravisWheelerLab/ULTRA

```
git clone https://github.com/TravisWheelerLab/ULTRA
cd ULTRA
cmake .
make
```

Binary: `dependencies/ULTRA/ultra`.
Script: `ultra.sh`, which runs `ultra --threads 1 --period 6 --bed --out res.bed <fasta>`.

### Dot2dot

https://github.com/Gege7177/Dot2dot

```
git clone https://github.com/Gege7177/Dot2dot
```

The repo ships prebuilt binaries, so there is nothing to compile. The script uses
`dependencies/Dot2dot/executables/dot.linux`.

Dot2dot also needs a config file at `dependencies/dot2dot.cfg`. It sits inside the
git-ignored `dependencies/` directory, so create it yourself:

```
cat > dot2dot.cfg <<'EOF'
FilterType = THRESHOLD
MinTRLen = 12
MinPurity = 0.1
AllowOverlap = Y
AA = 1
CC = 1
GG = 1
TT = 1
EOF
```

Script: `dot2dot.sh`, which runs `dot.linux --threads 1 --minmotif 1 --maxmotif 6 --minmatch 1
--maxgaps 0 --maxinsert 0 --config dot2dot.cfg`.

### Pytrf

```
pip install -U pytrf
```

Script: `pytrf.sh`, which runs `pytrf findstr -r 12 6 4 3 3 2 --out-format tsv`.

### PERF

```
pip install perf_ssr
```

Script: `perf.sh`, which runs `PERF --threads 1 --min-motif-size 1 --max-motif-size 6 --min-length 12`.

### Etandem (EMBOSS)

```
conda install -c conda-forge -c bioconda emboss
```

Script: `etandem.sh`, which runs `etandem -minrepeat 2 -maxrepeat 6 -threshold 6 -outfile res.etandem`.

### Non-B GFA (STR mode)

Build non-B GFA once under `src/general/` (see
[src/general/README.md](../general/README.md)).

Script: `gfa.sh`, which runs `gfa -seq <fasta> -out gfa_out` with every structure type
except STRs skipped (`-skipAPR -skipZ -skipDR -skipMR -skipIR -skipGQ
-skipSlipped -skipCruciform -skipTriplex -skipWGET`).

## Running the benchmarks

Run from the repository root with the `nonb-tools` env active. `NRUNS` is
optional and defaults to 1:

```
bash src/dr_and_str/<tool>.sh [NRUNS]
```

Output goes to `results/dr_and_str/<Tool>/run_<N>/` and the `/usr/bin/time -v`
report to `benchmarks/dr_and_str/<Tool>/run_<N>.txt`. `<Tool>` is one of
`TRF`, `Mreps`, `ULTRA`, `Dot2dot`, `Pytrf`, `PERF`, `Etandem`, `Non-B GFA STR`.
