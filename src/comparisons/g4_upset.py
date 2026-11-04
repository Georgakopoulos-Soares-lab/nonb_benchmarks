
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import eunoia as eu
import pyranges1 as pr
from functools import reduce
from itertools import combinations
from upsetplot import UpSet
import warnings
import numpy as np

warnings.filterwarnings("ignore")

base_path = Path("../../results")

g4_im_grinder_res = pd.read_csv(
    base_path / "g4" / "G4-iM Grinder" / "run_1" / "res.csv"
)

g4_im_grinder_res = g4_im_grinder_res[['Start', 'Finish']].rename(columns = {'Finish': "End"})
g4_im_grinder_res["Chromosome"] = "chr18"

g4_im_grinder_pr = pr.PyRanges(g4_im_grinder_res).merge_overlaps()

g4boost_res = pd.read_csv(
    base_path / "g4" / "G4Boost" / "run_1" / "clean_chr18.fa.gff",
    sep = '\t',
    header = None,
    usecols = [1, 2]
)

g4boost_res = g4boost_res.rename(columns={1: "Start", 2: "End"})
g4boost_res["Chromosome"] = "chr18"

g4boost_pr = pr.PyRanges(g4boost_res).merge_overlaps()

g4catchall_res = pd.read_csv(
    base_path / "g4" / "G4Catchall" / "run_1" / "res.txt",
    sep='\t',
    header=None,
    usecols=[1,2],
    names=["Start", "End"]
)

g4catchall_res['Chromosome'] = "chr18"

g4catchall_pr = pr.PyRanges(g4catchall_res).merge_overlaps()


g4hunter_res = pd.read_csv(
    base_path / "g4" / "G4Hunter" / "run_1" / "clean_chr18_pG4s.g4_hunter.tsv",
    sep = '\t'
)

g4hunter_res = g4hunter_res[['start', 'end']].rename(columns = {"start": "Start", 'end': "End"})
g4hunter_res["Chromosome"] = "chr18"

g4hunter_pr = pr.PyRanges(g4hunter_res).merge_overlaps()


g4mismatch_res = pd.read_csv(
    base_path / "g4" / "G4mismatch" / "run_1" / "scan_res.bedGraph",
    sep='\t',
    header= None,
    usecols=[1,2],
    names=['Start', 'End']
)

g4mismatch_res['Chromosome'] = "chr18"
g4mismatch_pr = pr.PyRanges(g4mismatch_res).merge_overlaps()


g4predict_res = pd.read_csv(
    base_path / "g4" / "G4predict" / "run_1" / "res.bed",
    sep='\t',
    header= None,
    usecols=[1,2],
    names=['Start', 'End']
)

g4predict_res['Chromosome'] = "chr18"
g4predict_pr = pr.PyRanges(g4predict_res).merge_overlaps()


imgqfinder_res = pd.read_csv(
    base_path / "g4" / "ImGQfinder" / "NC_060942.1_quadruplexes.csv",
    sep='\t',
    usecols=["Q1-Start", "Q4-Start", "Q4-Length"]
)

imgqfinder_res['End'] = imgqfinder_res['Q4-Start'] + imgqfinder_res['Q4-Length']
imgqfinder_res = imgqfinder_res.rename(columns={"Q1-Start": "Start"})
imgqfinder_res = imgqfinder_res[['Start', 'End']]
imgqfinder_res['Chromosome'] = "chr18"

imgqfinder_pr = pr.PyRanges(imgqfinder_res).merge_overlaps()


nonb_gfa_g4_res = pd.read_csv(
    base_path / "g4" / "Non-B GFA G4" / "run_1" / "gfa_out_GQ.tsv",
    sep = '\t'
)

nonb_gfa_g4_res = nonb_gfa_g4_res[['Start', 'Stop']].rename(columns = {'Stop': "End"})

nonb_gfa_g4_res["Chromosome"] = "chr18"

nonb_gfa_g4_pr = pr.PyRanges(nonb_gfa_g4_res).merge_overlaps()


pqsfinder_res = pd.read_csv(
    base_path / "g4" / "Pqsfinder" / "run_1" / "res.bed",
    sep = '\t',
    header = None,
    usecols = [1, 2]
)

pqsfinder_res = pqsfinder_res.rename(columns={1: "Start", 2: "End"})
pqsfinder_res["Chromosome"] = "chr18"

pqsfinder_pr = pr.PyRanges(pqsfinder_res).merge_overlaps()


qparse_res = pd.read_csv(
    base_path / "g4" / "QPARSE" / "run_1" / "res.txt",
    sep='\t',
    skiprows=2,
    usecols=[2,3],
    names=['Start', 'End']
)

qparse_res["Chromosome"] = 'chr18'
qparse_pr = pr.PyRanges(qparse_res).merge_overlaps()


quadparser_res = pd.read_csv(
    base_path / "g4" / "Quadparser" / "run_1" / "clean_chr18_pG4s.g4_hunter.tsv",
    sep = '\t'
)

quadparser_res = quadparser_res[['start', 'end']].rename(columns = {"start": "Start", 'end': "End"})
quadparser_res["Chromosome"] = "chr18"

quadparser_pr = pr.PyRanges(quadparser_res).merge_overlaps()


quadron_df_data = []

with open(base_path / "g4" / "Quadron" / "run_1" / "res.bed", "r", encoding="utf-8") as file:
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
    "G4-iM Grinder": g4_im_grinder_pr,
    'G4Boost': g4boost_pr,
    'G4Catchall': g4catchall_pr,
    'G4Hunter': g4hunter_pr,
    'G4mismatch': g4mismatch_pr,
    'G4predict': g4predict_pr,
    'ImGQfinder': imgqfinder_pr,
    'Non-B GFA': nonb_gfa_g4_pr,
    'Pqsfinder': pqsfinder_pr,
    "QPARSE": qparse_pr,
    "Quadparser": quadparser_pr,
    'Quadron': quadron_pr,
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
set_cols = g4_upset_data.select_dtypes(include="bool").columns.tolist()
g4_upset_data = g4_upset_data.set_index(set_cols)

fig = plt.figure(figsize=(10.25,4))

g4_upset = UpSet(
    g4_upset_data,
    orientation="horizontal",
    subset_size="sum",
    sum_over="bp",
    show_counts=False,
    sort_by = "degree",
    facecolor = "#838EA8",
    totals_plot_elements=0,
    element_size=None,
    min_subset_size=1
)

axes = g4_upset.plot(fig=fig)

for bar in axes["intersections"].patches:
    bar.set_edgecolor("black")
    bar.set_linewidth(1)

axes["intersections"].set_yscale("log")

for collection in axes["matrix"].collections:
    if hasattr(collection, "set_sizes"):
        collection.set_sizes([40])

axes["matrix"].tick_params(axis="y", labelsize=8)
axes["intersections"].tick_params(axis="y", labelsize=6)

axes["intersections"].set_ylabel("Number of\nnucleotides (kbp)", fontsize=8)

fig.savefig(
    base_path / "plots" / "g4_upset.pdf",
    transparent = True,
    bbox_inches = "tight",
    pad_inches = 0.02
)

plt.close()