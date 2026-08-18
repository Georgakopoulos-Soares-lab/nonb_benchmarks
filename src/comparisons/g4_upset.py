import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import eunoia as eu
import pyranges1 as pr
from functools import reduce
from itertools import combinations
from upsetplot import UpSet

base_path = Path("../results")

g4hunter_res = pd.read_csv(
    base_path / "g4" / "g4hunter" / "run_1" / "clean_chr18_pG4s.g4_hunter.tsv",
    sep = '\t'
)

g4hunter_res = g4hunter_res[['start', 'end']].rename(columns = {"start": "Start", 'end': "End"})
g4hunter_res["Chromosome"] = "chr18"

g4hunter_pr = pr.PyRanges(g4hunter_res).merge_overlaps()

g4boost_res = pd.read_csv(
    base_path / "g4" / "g4boost" / "run_1" / "clean_chr18.fa.gff",
    sep = '\t',
    header = None,
    usecols = [1, 2]
)

g4boost_res = g4boost_res.rename(columns={1: "Start", 2: "End"})
g4boost_res["Chromosome"] = "chr18"

g4boost_pr = pr.PyRanges(g4boost_res).merge_overlaps()

pqsfinder_res = pd.read_csv(
    base_path / "g4" / "pqsfinder" / "run_1" / "res.bed",
    sep = '\t',
    header = None,
    usecols = [1, 2]
)

pqsfinder_res = pqsfinder_res.rename(columns={1: "Start", 2: "End"})
pqsfinder_res["Chromosome"] = "chr18"

pqsfinder_pr = pr.PyRanges(pqsfinder_res).merge_overlaps()

quadron_df_data = []

with open(base_path / "g4" / "quadron" / "run_1" / "res.bed", "r", encoding="utf-8") as file:
    for line in file:
        if line.startswith("DATA:"):
            fields = line.strip().split()
            start = fields[1]
            length = fields[3]
            quadron_df_data.append((start, length))

quadron_res = pd.DataFrame(quadron_df_data, columns=["Start", "Length"])
quadron_res['Chromosome'] = "chr18"
quadron_res['Start'] = quadron_res['Start'].astype(int)
quadron_res['Length'] = quadron_res['Length'].astype(int)

quadron_res['End'] = quadron_res['Start'] + quadron_res['Length']

quadron_pr = pr.PyRanges(quadron_res).merge_overlaps()

sources = {
    'G4Hunter': g4hunter_pr,
    'G4Boost': g4boost_pr,
    'Quadron': quadron_pr,
    'Pqsfinder': pqsfinder_pr
}

names = list(sources.keys())
name_set = set(names)

rows = []

for r in range(1, len(names) + 1):
    for combo in combinations(names, r):

        region = reduce(
            lambda a, b: a.intersect_overlaps(b),
            (sources[n] for n in combo)
        )

        for excluded in name_set - set(combo):
            region = region.subtract_overlaps(sources[excluded])

        region = region.merge_overlaps()

        bp = float(region.lengths().sum())

        row = {name: name in combo for name in names}
        row["bp"] = round(bp / 1000, 2)

        rows.append(row)

g4_upset_data = pd.DataFrame(rows)
g4_upset_data = g4_upset_data.set_index(["G4Hunter", "G4Boost", "Quadron", "Pqsfinder"])

fig = plt.figure(figsize=(8, 2.5))

g4_upset = UpSet(
    g4_upset_data,
    subset_size="sum",
    sum_over="bp",
    show_counts=True,
    sort_by = "degree",
    facecolor = "#838EA8",
    totals_plot_elements=0,
    element_size=None
)

axes = g4_upset.plot(fig=fig)

for bar in axes["intersections"].patches:
    bar.set_edgecolor("black")
    bar.set_linewidth(1)

axes["intersections"].set_yscale("log")

for collection in axes["matrix"].collections:
    if hasattr(collection, "set_sizes"):
        collection.set_sizes([60])

axes["matrix"].tick_params(axis="y", labelsize=8)

axes["intersections"].tick_params(axis="y", labelsize=6)

axes["intersections"].yaxis.label.set_fontsize(8)

for text in axes["intersections"].texts:
    text.set_fontsize(6)


plt.savefig(
    base_path / "plots" / "g4_upset.pdf",
    transparent = True,
    bbox_inches = "tight",
    pad_inches = 0.02
)

plt.close()