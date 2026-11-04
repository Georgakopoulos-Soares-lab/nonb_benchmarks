
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from upsetplot import UpSet
import pyranges1 as pr
from functools import reduce
from itertools import combinations
import xml.etree.ElementTree as ET
import warnings

warnings.filterwarnings("ignore")

base_path = Path("../../results")

dot2dot_res = pd.read_csv(
    base_path / "dr_and_str" / "Dot2dot" / "run_1" / "res.bed",
    sep = '\t',
    usecols=['Start', 'End']
)

dot2dot_res['Chromosome'] = "chr18"
dot2dot_pr = pr.PyRanges(dot2dot_res).merge_overlaps()

etandem_res = pd.read_csv(
    base_path / "dr_and_str" / "Etandem" / "run_1" / "res.etandem",
    sep='\\s+',
    comment = "#"
)

etandem_res = etandem_res[['Start', 'End']]

etandem_res["Chromosome"] = "chr18"

etandem_pr = pr.PyRanges(etandem_res).merge_overlaps()


mreps_root = ET.parse(
   base_path / "dr_and_str" / "Mreps" / "run_1" / "res.xml"
).getroot()

results = []

for repeat in mreps_root.iter("repeat"):
    results.append({
        "start": repeat.findtext("start"),
        "end": repeat.findtext("end"),
        "period": repeat.findtext("period"),
        "exponent": repeat.findtext("exponent"),
        "sequence": repeat.findtext("sequence"),
    })

mreps_res = pd.DataFrame(results)

mreps_res = mreps_res[['start', 'end']].rename(columns = {'start':'Start', 'end': "End"})

mreps_res['Start'] = mreps_res['Start'].astype("int")
mreps_res['End'] = mreps_res['End'].astype("int")

mreps_res["Chromosome"] = "chr18"

mreps_pr = pr.PyRanges(mreps_res).merge_overlaps()


nonb_gfa_res = pd.read_csv(
    base_path / "dr_and_str" / "Non-B GFA STR" / "run_1" / "gfa_out_STR.tsv",
    sep = '\t'
)

nonb_gfa_res = nonb_gfa_res[['Start', 'Stop']].rename(columns = {'Stop': "End"})

nonb_gfa_res["Chromosome"] = "chr18"

nonb_gfa_pr = pr.PyRanges(nonb_gfa_res).merge_overlaps()


perf_res = pd.read_csv(
    base_path / "dr_and_str" / "PERF" / "run_1" / "res.txt",
    sep = '\t',
    header=None,
    usecols=[1, 2],
    names=['Start', 'End']
)

perf_res["Chromosome"] = "chr18"

perf_pr = pr.PyRanges(perf_res).merge_overlaps()


pytrf_res = pd.read_csv(
    base_path / "dr_and_str" / "Pytrf" / "run_1" / "res.txt",
    sep = '\t',
    header=None,
    usecols=[1, 2],
    names=['Start', 'End']
)

pytrf_res["Chromosome"] = "chr18"

pytrf_pr = pr.PyRanges(pytrf_res).merge_overlaps()

trf_res = pd.read_csv(
    base_path / "dr_and_str" / "trf" / "run_1" / "clean_chr18.fa.2.7.7.80.10.24.6.dat",
    skiprows = 13,
    header = None,
    sep = '\\s+',
    usecols=[0, 1],
    names=["Start", "End"],
    dtype={"Start": int, "End": int}
)

trf_res['Chromosome'] = "chr18"
trf_pr = pr.PyRanges(trf_res).merge_overlaps()

ultra_res = pd.read_csv(
    base_path / "dr_and_str" / "ULTRA" / "run_1" / "res.bed",
    sep = '\t',
    header=None,
    usecols=[1, 2],
    names=['Start', 'End']
)

ultra_res["Chromosome"] = "chr18"

ultra_pr = pr.PyRanges(ultra_res).merge_overlaps()


sources = {
    'TRF': trf_pr,
    'Non-B GFA': nonb_gfa_pr,
    'Mreps': mreps_pr,
    'Etandem': etandem_pr,
    'Dot2dot': dot2dot_pr,
    'PERF': perf_pr,
    'Pytrf': pytrf_pr,
    'ULTRA': ultra_pr
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

str_upset_data = pd.DataFrame(rows)
set_cols = str_upset_data.select_dtypes(include="bool").columns.tolist()
str_upset_data = str_upset_data.set_index(set_cols)

str_upset_data.to_csv(
    base_path / "str_intresection.csv"
)

fig = plt.figure(figsize=(4.9, 6.5))

str_upset = UpSet(
    str_upset_data,
    orientation="vertical",
    subset_size="sum",
    sum_over="bp",
    show_counts=False,
    sort_by = "degree",
    facecolor = "#5B4C7E",
    totals_plot_elements=0,
    element_size=None,
    min_subset_size=1
)

axes = str_upset.plot(fig=fig)

for bar in axes["intersections"].patches:
    bar.set_edgecolor("black")
    bar.set_linewidth(0.5)

axes["intersections"].set_xscale("log")

for collection in axes["matrix"].collections:
    if hasattr(collection, "set_sizes"):
        collection.set_sizes([10])

axes["matrix"].tick_params(axis="x", labelsize=8)
plt.setp(
    axes["matrix"].get_xticklabels(),
    rotation=45,
    ha="left",
    rotation_mode="anchor",
)
axes["intersections"].tick_params(axis="x", labelsize=6)

axes["intersections"].set_xlabel("Number of nucleotides (kbp)", fontsize=8)

fig.savefig(
    base_path / "plots" / "str_upset.pdf",
    transparent = True,
    bbox_inches = "tight",
    pad_inches = 0.02
)

plt.close()