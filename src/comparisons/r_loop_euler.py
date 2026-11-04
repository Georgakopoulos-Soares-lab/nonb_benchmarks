import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import eunoia as eu
import pyranges1 as pr
from functools import reduce
from itertools import combinations

base_path = Path("../../results")

qmrlfs_finder_res = pd.read_csv(
    base_path / "r_loops" / "QmRLFS-finder" / "run_1" / "res.out.bed",
    sep="\t",
    header=None,
    usecols=[1,2, 5],
    names=['Start', 'End', 'Strand']
)
qmrlfs_finder_res = qmrlfs_finder_res[qmrlfs_finder_res['Strand'] == "+"]

qmrlfs_finder_res["Chromosome"] = "chr18"
qmrlfs_finder_pr = pr.PyRanges(qmrlfs_finder_res).merge_overlaps()

deeprlooppre_res = pd.read_csv(
    base_path / "r_loops" / "deepRloopPre" / "run_1" / "res_final_predict.bed",
    sep='\t',
    header=None,
    usecols=[1,2],
    names=["Start", "End"]
)

deeprlooppre_res["Chromosome"] = "chr18"
deeprlooppre_pr = pr.PyRanges(deeprlooppre_res).merge_overlaps()

rows = []

with open(base_path / "r_loops" / "DeepER" / "run_1" / "regions.txt") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line:
            continue
        region, *intervals = line.split("\t")
        intervals = [iv for iv in intervals if iv.strip()]
        if intervals:
            for iv in intervals:
                rows.append((region, iv.strip()))
        else:
            rows.append((region, None))

deeper_res = pd.DataFrame(rows, columns=["region", "interval"])

deeper_res[["bin_start", "bin_end"]] = deeper_res["region"].str.extract(r"^.+\((\d+)-(\d+)\)$")

deeper_res[["interval_start", "interval_end"]] = deeper_res["interval"].str.extract(r"^(\d+)-(\d+)$")

for c in ["bin_start", "bin_end", "interval_start", "interval_end"]:
    deeper_res[c] = deeper_res[c].astype("Int64")

deeper_res['Start'] = deeper_res['bin_start'] + deeper_res['interval_start']
deeper_res['End'] = deeper_res['bin_start'] + deeper_res['interval_end']

deeper_res['Chromosome'] = 'chr18'
deeper_res = deeper_res[['Chromosome', 'Start', 'End']]
deeper_res = deeper_res.dropna()
deeper_pr = pr.PyRanges(deeper_res).merge_overlaps()

sources = {
    'QmRLFS-finder': qmrlfs_finder_pr,
    'deepRloopPre': deeprlooppre_pr,
    'DeepER': deeper_pr
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

        r_loop_bps = float(region.lengths().sum() if len(region) else 0)

        venn_regions[f'{"&".join(str(tool) for tool in combo)}'] = round(r_loop_bps/1000, 2)
        row = {name: name in combo for name in names}
        row["bp"] = round(r_loop_bps / 1000, 2)

        rows.append(row)

rloop_upset_data = pd.DataFrame(rows)
set_cols = rloop_upset_data.select_dtypes(include="bool").columns.tolist()
rloop_upset_data = rloop_upset_data.set_index(set_cols)

fig, ax = plt.subplots(figsize=(4.5, 4.5))

fit = eu.euler(
    venn_regions,
    shape="ellipse"
)

fit.plot(
    colors = {
        "QmRLFS-finder": "#fab9a6",
        "deepRloopPre": "#f36c44",
        "DeepER": "#B2ADAB"
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

for t in ax.texts:
    try:
        v = float(t.get_text())
    except ValueError:
        continue
    t.set_text(f"{v:,.0f}")

plt.savefig(
    base_path / "plots" / "r_loops_euler.pdf",
    transparent = True,
    bbox_inches = "tight",
    pad_inches = 0.02
)
plt.close()