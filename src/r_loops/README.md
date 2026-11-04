# R-loops

This category covers tools that detect R-loop forming sequences (RLFS).

Cloned tools go in `src/r_loops/dependencies/` (git-ignored). Run the install
commands below from that directory:

```
mkdir -p src/r_loops/dependencies
cd src/r_loops/dependencies
```

## Tools

### QmRLFS-finder

https://github.com/piroonj/QmRLFS-finder. It needs Biopython.

```
git clone https://github.com/piroonj/QmRLFS-finder
```

Script: `qmrlfs.sh`. It runs `dependencies/QmRLFS-finder/QmRLFS-finder.py
--infile <fasta> --outfile res -bed`.

### DeepER

https://github.com/NjuChenlab/DeepER

```
git clone https://github.com/NjuChenlab/DeepER
pip install torch numpy
```

The trained model `DeepER-deploy/DeepER.pkl` comes with the repo.
Script: `DeepER.sh`. It upper-cases the FASTA (DeepER rejects soft-masked bases) and
then runs `DeepER-deploy/Script.py <fasta> DeepER.pkl forward res.txt 1`.

### deepRloopPre

https://github.com/PEHGP/deepRloopPre. Use mamba rather than conda here, because
conda stalls when updating the env.

```
git clone https://github.com/PEHGP/deepRloopPre
cd deepRloopPre
mamba env update -f ml.yaml
python setup.py install
wget http://bioinfor.kib.ac.cn/R-loopAtlas/deepRloopPre/model/hela_classification.hdf5
```

Model: `dependencies/deepRloopPre/hela_classification.hdf5` (pretrained on human
HeLa).
Script: `deeprlooppre.sh`. It runs `bin/deepRloopPredict.py --h5 hela_classification.hdf5 --fasta <fasta> --prefix res`.

## Running the benchmarks

Run from the repository root with the env each tool was installed into active.
`NRUNS` is optional and defaults to 1:

```
bash src/r_loops/<qmrlfs|DeepER|deeprlooppre>.sh [NRUNS]
```

Output goes to `results/r_loops/<Tool>/run_<N>/` and the `/usr/bin/time -v`
report to `benchmarks/r_loops/<Tool>/run_<N>.txt`. `<Tool>` is one of
`QmRLFS-finder`, `DeepER`, `deepRloopPre`.