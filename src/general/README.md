# Shared tools

## Non-B GFA

https://github.com/abcsFrederick/non-B_gfa

Non-B GFA finds several non-B structure types in one pass. It is benchmarked separately in each
category. Each category's `gfa.sh` turns off every structure type except its own
with `-skip*` flags:

| Script | Mode | Results directory |
|---|---|---|
| `src/g4/gfa.sh` | G4 | `Non-B GFA G4` |
| `src/z_dna/gfa.sh` | Z-DNA | `Non-B GFA Z-DNA` |
| `src/ir/gfa.sh` | IR | `Non-B GFA IR` |
| `src/dr_and_str/gfa.sh` | STR | `Non-B GFA STR` |

Build it once here (the directory is git-ignored):

```
cd src/general
git clone https://github.com/abcsFrederick/non-B_gfa
cd non-B_gfa
make
```

All four scripts use the binary at `src/general/non-B_gfa/gfa`.