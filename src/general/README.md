# General repeat / non-B structure finders

Tools benchmarked here aren't specific to a single non-B DNA structure family —
general repeat finders and the EMBOSS repeat-finding tools.

## Tools

### GenericRepeatFinder (GRF)

Get the latest version from https://github.com/bioinfolabmu/GenericRepeatFinder

```
tar zxf GenericRepeatFinder-1.0.2.tar.gz
cd GenericRepeatFinder-1.0.2/src
make
```

Binary is `GenericRepeatFinder-1.0.2/src/grf-main/grf-main`.

Run: `sbatch src/general/grf.sh`. Runs TIR detection:
`grf-main -i <fasta> -c 0 -o <outdir> --min_tr 10 -t 1`.

### non-B GFA (nonb-gfa)

```
git clone https://github.com/abcsFrederick/non-B_gfa
cd non-B_gfa/
make
```

Binary is `non-B_gfa/gfa`.

Run: `sbatch src/general/gfa.sh`. Invokes
`gfa -seq <fasta> -out gfa_out -skipAPR`.

### EMBOSS (etandem, einverted)

```
conda install -c conda-forge -c bioconda emboss
```

- `etandem` — run: `sbatch src/general/etandem.sh`. Invokes
  `etandem -sequence <fasta> -minrepeat 10 -maxrepeat 10 -outfile res.etandem`.
- `einverted` — run: `sbatch src/general/einverted.sh`. Invokes
  `einverted -sequence <fasta> -gap 12 -threshold 50 -match 3 -mismatch -4
  -outfile res.einverted -outseq res.inv.fa`.

## Running the benchmarks

Submit `sbatch src/general/<tool>.sh` from the repository root (`grf`, `gfa`,
`etandem`, `einverted`). Each script is a 5-task job array that runs the tool
once on `data/chr18.fa` per task, timed with `/usr/bin/time -v`. Output goes to
`results/general/<tool>/run_<N>/`, timing to
`benchmarks/general/<tool>/run_<N>.txt`, and SLURM logs to
`logs/general/<tool>/run_<N>.{out,err}` (the `gfa` job itself is named
`nonB_gfa` in its SLURM logs).
