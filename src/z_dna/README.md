# Z-DNA

This category covers tools that detect Z-DNA forming sequences.

Cloned tools and model files go in `src/z_dna/dependencies/` (git-ignored). Run
the install commands below from that directory:

```
mkdir -p src/z_dna/dependencies
cd src/z_dna/dependencies
```

## Tools

### ZSeeker

https://github.com/Georgakopoulos-Soares-lab/ZSeeker. It needs Python 3.11.

```
pip install ZSeeker
```

Script: `zseeker.sh`, which runs `ZSeeker --fasta <fasta> --n_jobs 1 --output_dir <dir>`.

### Z-Hunt

https://github.com/Ho-Lab-Colostate/zhunt

```
git clone https://github.com/Ho-Lab-Colostate/zhunt
cd zhunt
gcc -O2 -o bin/zhunt zhun3.c -lm
```

Binary: `dependencies/zhunt/bin/zhunt`.
Script: `zhunt.sh`. It strips the FASTA header and newlines into a single-line
sequence file and then runs `zhunt 12 6 12 <sequence>`.

### ZDNABERT

The inference code in `src/z_dna/zdnabert.py` is adapted from
https://github.com/mitiau/Z-DNABERT/blob/main/ZDNA-prediction.ipynb.

```
pip install transformers biopython gdown scipy
pip install torch --index-url https://download.pytorch.org/whl/cu126
```

Download the tokenizer/config files and model checkpoints into
`dependencies/Z-DNABERT/`:

```
mkdir -p Z-DNABERT && cd Z-DNABERT

# config.json, special_tokens_map.json, tokenizer_config.json, vocab.txt
gdown 10sF8Ywktd96HqAL0CwvlZZUUGj05CGk5
gdown 16bT7HDv71aRwyh3gBUbKwign1mtyLD2d
gdown 1EE9goZ2JRSD8UTx501q71lGCk-CK3kqG
gdown 1gZZdtAoDnDiLQqjQfGyuwt268Pe5sXW0

# model checkpoints (one per training set); the benchmark uses HG_kouzine
gdown 1dAeAt5Gu2cadwDhbc7OnenUgDLHlUvkx --output models/HG_kouzine/
gdown 1VAsp8I904y_J0PUhAQqpSlCn1IqfG0FB --output models/HG_chipseq/
gdown 1W6GEgHNoitlB-xXJbLJ_jDW4BF35W1Sd --output models/MM_curax/
gdown 1dXpQFmheClKXIEoqcZ7kgCwx6hzVCv3H --output models/MM_kouzine/
```

Script: `zdnabert.sh`. It copies the config, tokenizer, vocab and
`models/HG_kouzine/pytorch_model.bin` into a per-run model directory. It then runs
`python src/z_dna/zdnabert.py <model_dir> <fasta> res.txt`, which tokenizes the
sequence into 6-mers, runs `BertForTokenClassification` and reports regions above
a 0.5 confidence threshold. ZDNABERT is slow on CPU. `missing_jobs.sh` runs the
same loop under SBATCH headers (edit `--partition`/`--account` first) and is
submitted with `sbatch src/z_dna/missing_jobs.sh [NRUNS]`.

### Non-B GFA (Z-DNA mode)

Build non-B GFA once under `src/general/` (see
[src/general/README.md](../general/README.md)).

Script: `gfa.sh`, which runs `gfa -seq <fasta> -out gfa_out` with every structure type
except Z-DNA skipped.

## Running the benchmarks

Run from the repository root with the right env active. `NRUNS` is optional and
defaults to 1:

```
bash src/z_dna/<zseeker|zhunt|zdnabert|gfa>.sh [NRUNS]
```

Output goes to `results/z_dna/<Tool>/run_<N>/` and the `/usr/bin/time -v` report
to `benchmarks/z_dna/<Tool>/run_<N>.txt`. `<Tool>` is one of `ZSeeker`,
`Z-Hunt`, `ZDNABERT`, `Non-B GFA Z-DNA`.