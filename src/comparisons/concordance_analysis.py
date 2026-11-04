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
import re
import xml.etree.ElementTree as ET

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
        row["Kb"] = round(bp / 1000, 2)

        rows.append(row)

g4_data = pd.DataFrame(rows)
set_cols = g4_data.select_dtypes(include="bool").columns.tolist()
g4_data = g4_data.set_index(set_cols)

hseeker_res = pd.read_csv(
    base_path / "h_dna" / "HSeeker" / "run_1" / "res_HDNA.tsv",
    sep = '\t'
)

hseeker_res = hseeker_res[["start", "end"]].rename(columns={"start": "Start", "end": "End"})

hseeker_res['Chromosome'] = "chr18"
hseeker_pr = pr.PyRanges(hseeker_res).merge_overlaps()

triplex_res = pd.read_csv(
    base_path / "h_dna" / "Triplex" / "run_1" / "res.bed",
    sep = '\t',
    header = None,
    usecols=[1, 2]
)

triplex_res = triplex_res.rename(columns={1: "Start", 2: "End"})

triplex_res['Chromosome'] = "chr18"
triplex_pr = pr.PyRanges(triplex_res).merge_overlaps()

sources = {
    'HSeeker': hseeker_pr,
    'Triplex': triplex_pr
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

        h_dna_bps = float(region.lengths().sum() if len(region) else 0)

        venn_regions[f'{"&".join(str(tool) for tool in combo)}'] = round(h_dna_bps/1000, 2)
        row = {name: name in combo for name in names}
        row["Kb"] = round(h_dna_bps / 1000, 2)

        rows.append(row)

hdna_data = pd.DataFrame(rows)
set_cols = hdna_data.select_dtypes(include="bool").columns.tolist()
hdna_data = hdna_data.set_index(set_cols)

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
        row["Kb"] = round(bp / 1000, 2)

        rows.append(row)

ir_data = pd.DataFrame(rows)
set_cols = ir_data.select_dtypes(include="bool").columns.tolist()
ir_data = ir_data.set_index(set_cols)

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
        row["Kb"] = round(r_loop_bps / 1000, 2)

        rows.append(row)

rloop_data = pd.DataFrame(rows)
set_cols = rloop_data.select_dtypes(include="bool").columns.tolist()
rloop_data = rloop_data.set_index(set_cols)

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
        row["Kb"] = round(bp / 1000, 2)

        rows.append(row)

str_data = pd.DataFrame(rows)
set_cols = str_data.select_dtypes(include="bool").columns.tolist()
str_upset_data = str_data.set_index(set_cols)

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

# zdnabert_res = pd.read_csv(
#     base_path / "z_dna" / "zdnabert" / "run_1" / "res.txt",
#     skiprows=3,
#     header = None,
#     dtype={0: str}
# )

# stripped_lines = zdnabert_res[0].str.strip()
# line_midpoint = stripped_lines.str.len() // 2

# zdnabert_res['Start'] = [int(s[:m]) for s, m in zip(stripped_lines, line_midpoint)]
# zdnabert_res['End'] = [int(s[m:]) for s, m in zip(stripped_lines, line_midpoint)]

# zdnabert_res = zdnabert_res[["Start", "End"]]

# zdnabert_res['Chromosome'] = "chr18"

# zdnabert_pr = pr.PyRanges(zdnabert_res).merge_overlaps()

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
    # 'Z-DNABERT': zdnabert_pr,
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
        row["Kb"] = round(z_dna_bps / 1000, 2)

        rows.append(row)

zdna_data = pd.DataFrame(rows)
set_cols = zdna_data.select_dtypes(include="bool").columns.tolist()
zdna_data = zdna_data.set_index(set_cols)

with pd.ExcelWriter(base_path / 'concordance_results.xlsx') as writer:
    zdna_data.to_excel(writer, sheet_name='Z-DNA', index=True)
    g4_data.to_excel(writer, sheet_name='G-quadruplexes', index=True)
    rloop_data.to_excel(writer, sheet_name='R-loops', index=True)
    str_data.to_excel(writer, sheet_name='Short Tandem Repeats', index=True)
    ir_data.to_excel(writer, sheet_name='Inverted Repeats', index=True)
    hdna_data.to_excel(writer, sheet_name='H-DNA', index=True)