
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from upsetplot import UpSet
import pyranges1 as pr
from functools import reduce
from itertools import combinations
from Bio import SeqIO
import re
import warnings
warnings.filterwarnings("ignore")


base_path = Path("../../results")


nonb_gfa_ir_res = pd.read_csv(
    base_path / "ir" / "Non-B GFA IR" / "run_1" / "gfa_out_IR.tsv",
    sep = '\t'
)

nonb_gfa_ir_res = nonb_gfa_ir_res[['Start', 'Stop']].rename(columns = {'Stop': "End"})

nonb_gfa_ir_res["Chromosome"] = "chr18"

nonb_gfa_ir_pr = pr.PyRanges(nonb_gfa_ir_res).merge_overlaps()


irf_res = pd.read_csv(
    base_path / "ir" / "IRF" / "run_1" / "clean_chr18.fa.2.3.5.80.10.20.10000.101.dat",
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

detectir_pr = read_detectir_data(base_path / 'ir' / 'DetectIR' / 'run_1' / "perfect_repeats.fasta").merge_overlaps()


findir_pr = read_detectir_data(base_path / 'ir' / 'FindIR' / 'run_1' / "predictedIRs.fasta")


einverted_arm = re.compile(r"^\s*(\d+)\s+[A-Za-z-]+\s+(\d+)\s*$")

einverted_records = []
einverted_coords = []
with open(base_path / 'ir' / 'Einverted' / 'run_1' / "res.einverted") as f:
    for line in f:
        a = einverted_arm.match(line)
        if a:
            einverted_coords += [int(a.group(1)), int(a.group(2))]
            if len(einverted_coords) == 4:
                einverted_records.append(("chr18", min(einverted_coords) - 1, max(einverted_coords)))
                einverted_coords = []

einverted_records.sort(key=lambda r: (r[0], r[1]))

einverted_res = pd.DataFrame(einverted_records,columns=["Chromosome", "Start", "End"])
einverted_pr = pr.PyRanges(einverted_res).merge_overlaps()


def read_grf_data(res_path):
    data = []
    with open(res_path, "r") as file:
        for line in file:
            if line.startswith(">"):
                start = int(line.split(":")[1].strip())
                end = int(line.split(":")[2].strip())
                data.append([start, end])

    res = pd.DataFrame(data, columns = ["Start", "End"])

    res['Chromosome'] = "chr18"

    pr_object = pr.PyRanges(res).merge_overlaps()

    return pr_object

grf_spacers = read_grf_data(base_path / 'ir' / 'GRF' / 'run_1' / "perfect.spacer.fasta")
grf_arms = read_grf_data(base_path / 'ir' / 'GRF' / 'run_1' / "perfect.fasta")

grf_pr = pr.concat([grf_arms, grf_spacers]).merge_overlaps()


iupacpal_text = open(base_path / 'ir' / 'IUPACpal' / 'run_1' / "perfect.out").read()

pat = re.compile(r"^\s*(\d+)\s+\S+\s+(\d+)\s*\n.*\|.*\n\s*(\d+)\s+\S+\s+(\d+)\s*$", re.M)

iupacpal_res = pd.DataFrame([tuple(map(int, m.groups())) for m in pat.finditer(iupacpal_text)],
                  columns=["l_start", "l_end", "r_end", "r_start"])

iupacpal_res = pd.DataFrame({
    "Chromosome": "chr18",
    "Start": iupacpal_res.l_start,
    "End": iupacpal_res.r_end
})

iupacpal_pr = pr.PyRanges(iupacpal_res).merge_overlaps()


sources = {
    'IRF': irf_pr,
    'Non-B GFA': nonb_gfa_ir_pr,
    'DetectIR': detectir_pr,
    'FindIR': findir_pr,
    'Einverted': einverted_pr,
    'GRF': grf_pr,
    'IUPACpal': iupacpal_pr
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

ir_upset_data = pd.DataFrame(rows)
set_cols = ir_upset_data.select_dtypes(include="bool").columns.tolist()
ir_upset_data = ir_upset_data.set_index(set_cols)

ir_upset_data.to_csv(
    base_path / "ir_intresection.csv"
)

fig = plt.figure(figsize=(4.9, 6.5))

ir_upset = UpSet(
    ir_upset_data,
    orientation="vertical",
    subset_size="sum",
    sum_over="bp",
    show_counts=False,
    sort_by = "degree",
    facecolor = "#CAC3BD",
    totals_plot_elements=0,
    element_size=None,
    min_subset_size=1
)

axes = ir_upset.plot(fig=fig)

for bar in axes["intersections"].patches:
    bar.set_edgecolor("black")
    bar.set_linewidth(1)

axes["intersections"].set_xscale("log")

for collection in axes["matrix"].collections:
    if hasattr(collection, "set_sizes"):
        collection.set_sizes([40])

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
    base_path / "plots" / "ir_upset.pdf",
    transparent = True,
    bbox_inches = "tight",
    pad_inches = 0.02
)

plt.show()
