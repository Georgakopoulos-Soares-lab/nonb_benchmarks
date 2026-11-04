import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import eunoia as eu
import pyranges1 as pr
from functools import reduce
from itertools import combinations

base_path = Path("../../results")

zseeker_res = pd.read_csv(
    base_path / "z_dna" / "ZSeeker" / "run_1" / "clean_chr18_zdna_score.csv"
)[["Start", "End"]]

zseeker_res['Chromosome'] = "chr18"

zseeker_pr = pr.PyRanges(zseeker_res).merge_overlaps()

nonb_gfa_zdna_res = pd.read_csv(
    base_path / "z_dna" / "Non-B GFA Z-DNA" / "run_1" / "gfa_out_Z.tsv",
    sep = '\t'
)
nonb_gfa_zdna_res = nonb_gfa_zdna_res[['Start', 'Stop']].rename(columns={"Stop": "End"})

nonb_gfa_zdna_res['Chromosome'] = "chr18"
nonb_gfa_zdna_pr = pr.PyRanges(nonb_gfa_zdna_res).merge_overlaps()

zhunt_res = pd.read_csv(
    base_path / "z_dna" / "Z-Hunt" / "run_1" / "clean_chr18.fa.Z-SCORE",
    skiprows = 1,
    header = None,
    sep=r'\s+'
)

zhunt_res = zhunt_res.reset_index(drop=True)
zhunt_res['Start'] = zhunt_res.index.to_numpy()

zhunt_res["length"] = zhunt_res[3].str.len()
zhunt_res['End'] = zhunt_res['Start'] + zhunt_res['length']
zhunt_res = zhunt_res[zhunt_res[2] >= 500] 

zhunt_res['Chromosome'] = "chr18"

zhunt_res = zhunt_res[['Chromosome', 'Start', 'End']]

zhunt_pr = pr.PyRanges(zhunt_res).merge_overlaps()

sources = {
    'ZSeeker': zseeker_pr,
    'Z-Hunt II': zhunt_pr,
    'Non-B GFA': nonb_gfa_zdna_pr
}

names = list(sources.keys())
name_set = set(names)

venn_regions = {}
rows = []

for r in range(1, len(names) + 1):
    for combo in combinations(names, r):

        region = reduce(lambda a, b: a.intersect_overlaps(b), (sources[n] for n in combo))

        for excluded in name_set - set(combo):
            region = region.subtract_overlaps(sources[excluded])

        region = region.merge_overlaps()

        z_dna_bps = float(region.lengths().sum())

        venn_regions["&".join(tool for tool in combo)] = round(z_dna_bps/1000, 2)
        row = {name: name in combo for name in names}
        row["bp"] = round(z_dna_bps / 1000, 2)

        rows.append(row)

zdna_upset_data = pd.DataFrame(rows)
set_cols = zdna_upset_data.select_dtypes(include="bool").columns.tolist()
zdna_upset_data = zdna_upset_data.set_index(set_cols)

zdna_upset_data.to_csv(
    base_path / "zdna_intresection.csv"
)


fig, ax = plt.subplots(figsize=(3.5, 3.5))

fit = eu.euler(
    venn_regions,
    shape="ellipse"
)

fit.plot(
    colors = {
        "ZSeeker": "#F78FC7",
        "Z-Hunt II": "#C499B0",
        "Z-DNABERT": "#917785",
        "Non-B GFA": "#5F3B4E"
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
    base_path / "plots" / "z_dna_euler.pdf",
    transparent = True,
    bbox_inches = "tight",
    pad_inches = 0.02
)
plt.close()
