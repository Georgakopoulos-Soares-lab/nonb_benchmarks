# H-DNA / triplexes

This category covers tools that detect triplex-forming (H-DNA) sequences. Both tools are
run with repeat arms of 10–30 nt and spacers of up to 10 nt.

Both tools install from package managers, so there is no `dependencies/`
directory.

## Tools

### Triplex (Bioconductor)

```
conda install -c conda-forge -c bioconda bioconductor-rtracklayer bioconductor-genomicranges
```

In R:

```
if (!require("BiocManager", quietly = TRUE)) install.packages("BiocManager")
BiocManager::install("triplex")
```

Script: `triplex.sh`. It calls `src/h_dna/triplex.R`, which runs
`triplex.search(seq, min_len = 10, max_len = 30, min_loop = 1, max_loop = 10)`
and writes `res.bed`.

### HSeeker

```
pip install hseeker
```

Script: `hseeker.sh`, which runs `hseeker -workers 1 -minrep 10 -maxrep 30 -maxspacer 10`.

## Running the benchmarks

Run from the repository root with the `nonb-tools` env active. `NRUNS` is
optional and defaults to 1:

```
bash src/h_dna/<triplex|hseeker>.sh [NRUNS]
```

Output goes to `results/h_dna/<Tool>/run_<N>/` and the `/usr/bin/time -v` report
to `benchmarks/h_dna/<Tool>/run_<N>.txt`. `<Tool>` is `Triplex` or `HSeeker`.
