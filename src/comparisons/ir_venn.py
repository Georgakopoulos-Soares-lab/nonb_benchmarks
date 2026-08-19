import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import eunoia as eu
import pyranges1 as pr
from functools import reduce
from itertools import combinations

base_path = Path("../../results")

nonb_gfa_ir_res = pd.read_csv(
    base_path / "general" / "gfa" / "run_1" / "gfa_out_IR.tsv",
    sep = '\t'
)

nonb_gfa_ir_res = nonb_gfa_ir_res[['Start', 'Stop']].rename(columns = {'Stop': "End"})

nonb_gfa_ir_res["Chromosome"] = "chr18"

nonb_gfa_ir_pr = pr.PyRanges(nonb_gfa_ir_res).merge_overlaps()

irf_res = pd.read_csv(
    base_path / "ir" / "irf" / "run_1" / "clean_chr18.fa.2.3.5.80.10.20.100000.1000000.dat",
    skiprows = 13,
    header = None,
    sep = '\\s+',
    usecols=[0, 1],
    names=["Start", "End"],
    dtype={"Start": int, "End": int}
)

irf_res['Chromosome'] = "chr18"
irf_pr = pr.PyRanges(irf_res).merge_overlaps()

def read_detectir_data(res_path):
    data = []
    with open(res_path, "r") as file:
        for line in file:
            if line.startswith(">"):
                start = int(line.split("|")[0][1:])
                length = int(line.split("|")[1].strip())
                data.append([start, length])

    res = pd.DataFrame(data, columns = ["Start", "Length"])

    res['Chromosome'] = "chr18"
    res['End'] = res['Start'] + res['Length']

    pr_object = pr.PyRanges(res).merge_overlaps()

    return pr_object

detectir_pr = pr.concat([
    read_detectir_data(base_path / 'ir' / 'detectir' / 'run_1' / "imperfect_repeats.fasta"),
    read_detectir_data(base_path / 'ir' / 'detectir' / 'run_1' / "perfect_repeats.fasta")
]).merge_overlaps()

matlabir_pr = read_detectir_data(base_path / 'ir' / 'matlabir' / 'run_1' / "predictedIRs.fasta")

sources = {
    'IRF': irf_pr,
    'Non-B GFA': nonb_gfa_ir_pr,
    'detectIR': detectir_pr,
    'MATLAB-based IR tool': matlabir_pr
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
        "IRF": "#5E3C4F",
        "detectIR": "#62979C",
        "MATLAB-based IR tool": "#9C9462",
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
    base_path / "plots" / "ir_venn.pdf",
    transparent = True,
    bbox_inches = "tight",
    pad_inches = 0.02
)

plt.close()
