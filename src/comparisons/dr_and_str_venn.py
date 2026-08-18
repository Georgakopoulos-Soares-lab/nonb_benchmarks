import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import eunoia as eu
import pyranges1 as pr
from functools import reduce
from itertools import combinations
import xml.etree.ElementTree as ET

base_path = Path("../../results")

nonb_gfa_dr_res = pd.read_csv(
    base_path / "general" / "gfa" / "run_1" / "gfa_out_DR.tsv",
    sep = '\t'
)

nonb_gfa_dr_res = nonb_gfa_dr_res[['Start', 'Stop']].rename(columns = {'Stop': "End"})

nonb_gfa_dr_res["Chromosome"] = "chr18"

nonb_gfa_dr_pr = pr.PyRanges(nonb_gfa_dr_res).merge_overlaps()

nonb_gfa_str_res = pd.read_csv(
    base_path / "general" / "gfa" / "run_1" / "gfa_out_STR.tsv",
    sep = '\t'
)

nonb_gfa_str_res = nonb_gfa_str_res[['Start', 'Stop']].rename(columns = {'Stop': "End"})

nonb_gfa_str_res["Chromosome"] = "chr18"

nonb_gfa_str_pr = pr.PyRanges(nonb_gfa_str_res).merge_overlaps()

nonb_gfa_pr = pr.concat([nonb_gfa_dr_pr, nonb_gfa_str_pr]).merge_overlaps()

etandem_res = pd.read_csv(
    base_path / "general" / "etandem" / "run_1" / "res.etandem",
    sep='\\s+',
    comment = "#"
)

etandem_res = etandem_res[['Start', 'End']]

etandem_res["Chromosome"] = "chr18"

etandem_pr = pr.PyRanges(etandem_res).merge_overlaps()

mreps_root = ET.parse(
   base_path / "dr_and_str" / "mreps" / "run_1" / "res.xml"
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

trf_res = pd.read_csv(
    base_path / "dr_and_str" / "trf" / "run_1" / "clean_chr18.fa.2.7.7.80.10.50.500.dat",
    skiprows = 13,
    header = None,
    sep = '\\s+',
    usecols=[0, 1],
    names=["Start", "End"],
    dtype={"Start": int, "End": int}
)

trf_res['Chromosome'] = "chr18"
trf_pr = pr.PyRanges(trf_res).merge_overlaps()


sources = {
    'TRF': trf_pr,
    'Non-B GFA': nonb_gfa_pr,
    'Mreps': mreps_pr,
    'Etandem': etandem_pr
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

        bps = float(region.lengths().sum() if len(region) else 0)

        venn_regions[f'{"&".join(str(tool) for tool in combo)}'] = round(bps/1000, 2)

fig, ax = plt.subplots(figsize=(3.5, 3.5))

fit = eu.venn(
    venn_regions,
    shape="ellipse"
)

fit.plot(
    colors = {
        "TRF": "#5E3C4F",
        "Mreps": "#62979C",
        "Etandem": "#9C9462",
        "Non-B GFA": "black"
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
    base_path / "plots" / "dr_and_str_venn.pdf",
    transparent = True,
    bbox_inches = "tight",
    pad_inches = 0.02
)

plt.close()