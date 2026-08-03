# Z-DNA

Tools benchmarked here detect Z-DNA forming sequences.

## Tools

### ZSeeker

From https://github.com/Georgakopoulos-Soares-lab/ZSeeker

```
# python 3.11
pip install ZSeeker
```

Run: `sbatch src/z_dna/zseeker.sh`. Invokes
`ZSeeker --fasta <fasta> --n_jobs 1 --output_dir <dir>`.

### Z-HUNT (zhunt)

From https://github.com/Ho-Lab-Colostate/zhunt

```
git clone https://github.com/Ho-Lab-Colostate/zhunt
cd zhunt
gcc -O2 -o bin/zhunt zhun3.c -lm
```

Expected at `src/z_dna/dependencies/zhunt/bin/zhunt`.

Run: `sbatch src/z_dna/zhunt.sh`. The script strips FASTA headers/newlines into
a single-line sequence file before running
`zhunt 12 6 12 <linearized_fasta>`.

### Z-DNABERT

Code from
https://github.com/mitiau/Z-DNABERT/blob/main/ZDNA-prediction.ipynb

```
pip install transformers biopython gdown scipy
pip install torch --index-url https://download.pytorch.org/whl/cu126
```

Download the model checkpoints (one directory per training condition):

```
gdown 1VAsp8I904y_J0PUhAQqpSlCn1IqfG0FB --output models/HG_chipseq/
gdown 1dAeAt5Gu2cadwDhbc7OnenUgDLHlUvkx --output models/HG_kouzine/
gdown 1W6GEgHNoitlB-xXJbLJ_jDW4BF35W1Sd --output models/MM_curax/
gdown 1dXpQFmheClKXIEoqcZ7kgCwx6hzVCv3H --output models/MM_kouzine/

gdown 10sF8Ywktd96HqAL0CwvlZZUUGj05CGk5
gdown 16bT7HDv71aRwyh3gBUbKwign1mtyLD2d
gdown 1EE9goZ2JRSD8UTx501q71lGCk-CK3kqG
gdown 1gZZdtAoDnDiLQqjQfGyuwt268Pe5sXW0
```

Run: `sbatch src/z_dna/zdnabert.sh` (GPU partition). Assembles a model
directory from `src/z_dna/dependencies/Z-DNABERT/` (config, tokenizer,
vocab, and the `HG_chipseq` checkpoint) and runs
`python src/z_dna/zdnabert.py <model_dir> <fasta> <output.txt>`, which tokenizes
the sequence into 6-mers, runs it through `BertForTokenClassification` on GPU,
and reports Z-DNA candidate regions above a 0.5 confidence threshold.

### Z-GENIE

From https://github.com/agarzare/Z-GENIE

```
git clone https://github.com/agarzare/Z-GENIE.git
install.packages("devtools")
devtools::install("ZGENIE")
```

Vendored under `src/z_dna/dependencies/Z-GENIE`; not yet wired up to a
benchmark script.

### DeepZ

```
git clone https://github.com/Nazar1997/DeepZ_data_creation
```

Vendored under `src/z_dna/dependencies/DeepZ_data_creation`; not yet wired up
to a benchmark script.

## Running the benchmarks

Submit `sbatch src/z_dna/<tool>.sh` from the repository root (`zseeker`,
`zhunt`, `zdnabert`). Each script is a 5-task job array that runs the tool once
on `data/chr18.fa` per task, timed with `/usr/bin/time -v`. `zdnabert` is
submitted to a GPU partition; the others to CPU.

Output/timing/log paths are not fully consistent between scripts:
- `zdnabert.sh` follows the repo-wide convention:
  `results/z_dna/zdnabert/run_<N>/`, `benchmarks/z_dna/zdnabert/run_<N>.txt`,
  `logs/z_dna/zdnabert/run_<N>.{out,err}`.
- `zseeker.sh` and `zhunt.sh` write results/benchmarks under `z_dna` but SLURM
  logs under `zdna` (no underscore) — e.g. `zhunt.sh` uses
  `results/zdna/zhunt/run_<N>/` and `benchmarks/zdna/zhunt/run_<N>.txt`, but
  `logs/zdna/zhunt/run_<N>.{out,err}`. Since only `logs/z_dna/` exists at the
  top level, submitting these two as-is will fail unless `logs/zdna/<tool>/` is
  created first (or the scripts are fixed to use `z_dna` consistently).
