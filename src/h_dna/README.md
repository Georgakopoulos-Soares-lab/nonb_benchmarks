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
