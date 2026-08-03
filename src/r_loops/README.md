# R-loops

Tools benchmarked here detect R-loop forming sequences (RLFS).

## Tools

### QmRLFS-finder

From https://github.com/piroonj/QmRLFS-finder

```
git clone https://github.com/piroonj/QmRLFS-finder
```

Requires Biopython 1.64 and Python.

Run: `sbatch src/r_loops/qmrlfs.sh`. Invokes
`python QmRLFS-finder.py -i <fasta> -o res.tsv`.

## Running the benchmarks

Submit `sbatch src/r_loops/qmrlfs.sh` from the repository root. It's a 5-task
job array that runs QmRLFS-finder once on `data/chr18.fa` per task, timed with
`/usr/bin/time -v`. Output goes to
`results/r_loops/qmrlfs_finder/run_<N>/`, timing to
`benchmarks/r_loops/qmrlfs_finder/run_<N>.txt`, and SLURM logs to
`logs/r_loops/qmrlfs_finder/run_<N>.{out,err}`.
