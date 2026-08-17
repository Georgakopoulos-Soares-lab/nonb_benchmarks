import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import eunoia as eu
import pyranges1 as pr
from functools import reduce
from itertools import combinations

base_path = Path("../../results")

hseeker_res = pd.read_csv(
    base_path / "h_dna" / "hseeker" / "run_1" / "res_HDNA.tsv",
    sep = '\t'
)

hseeker_res = hseeker_res[["start", "end"]].rename(columns={"start": "Start", "end": "End"})

hseeker_res['Chromosome'] = "chr18"
hseeker_pr = pr.PyRanges(hseeker_res).merge_overlaps()

triplex_res = pd.read_csv(
    base_path / "h_dna" / "triplex" / "run_1" / "res.bed",
    sep = '\t',
    header = None,
    usecols=[1, 2]
)

triplex_res = triplex_res.rename(columns={1: "Start", 2: "End"})

triplex_res['Chromosome'] = "chr18"
triplex_pr = pr.PyRanges(triplex_res).merge_overlaps()

triplexator_res = pd.read_csv(
    base_path / "h_dna" / "triplexator" / "run_1" / "res.bed",
    sep = '\t',
    header = None,
    skiprows = 1,
    usecols = [1, 2]
)

triplexator_res = triplexator_res.rename(columns={1: "Start", 2: "End"})

triplexator_res['Chromosome'] = "chr18"
triplexator_pr = pr.PyRanges(triplexator_res).merge_overlaps()

sources = {
    'HSeeker': hseeker_pr,
    'Triplex': triplex_pr,
    'Triplexator': triplexator_pr
}

names = list(sources.keys())
name_set = set(names)

venn_regions = {}

for r in range(1, len(names) + 1):
    for combo in combinations(names, r):

        region = reduce(lambda a, b: a.intersect_overlaps(b), (sources[n] for n in combo))

        for excluded in name_set - set(combo):
            region = region.subtract_overlaps(sources[excluded])

        region = region.merge_overlaps()

        z_dna_bps = float(region.lengths().sum() if len(region) else 0)

        venn_regions[f'{"&".join(str(tool) for tool in combo)}'] = round(z_dna_bps/1000, 2)

fig, ax = plt.subplots(figsize=(3.5, 3.5))

fit = eu.euler(
    venn_regions,
    shape="ellipse"
)

fit.plot(
    colors = {
        "HSeeker": "#5E3C4F",
        "Triplexator": "#62979C",
        "Triplex": "#9C9462"
    },
    edges = {
        "linewidth": 0.75,
        "alpha": 1
    },
    labels={
        "fontsize": 7
    },
    quantities={
        "type": [
            "counts"
        ],
        "fontsize": 6,
        "color": "black"
    },
    ax=ax
)

plt.savefig(
    base_path / "plots" / "h_dna_euler.pdf",
    transparent = True,
    bbox_inches = "tight",
    pad_inches = 0.02
)
plt.close()
