import numpy as np
import pandas as pd
from pathlib import Path
from matplotlib_venn import venn3, venn3_circles
import matplotlib.pyplot as plt
import pyranges1 as pr

base_path = Path("../../results")

zseeker_res = pd.read_csv(
    base_path / "z_dna" / "zseeker" / "run_1" / "chr18_zdna_score.csv"
)[["Start", "End"]]

zseeker_res['Chromosome'] = "chr18"

zseeker_pr = pr.PyRanges(zseeker_res).merge_overlaps()

zdnabert_res = pd.read_csv(
    base_path / "z_dna" / "zdnabert" / "run_1" / "res.txt",
    skiprows=3,
    header = None,
    dtype={0: str}
)

stripped_lines = zdnabert_res[0].str.strip()
line_midpoint = stripped_lines.str.len() // 2

zdnabert_res['Start'] = [int(s[:m]) for s, m in zip(stripped_lines, line_midpoint)]
zdnabert_res['End'] = [int(s[m:]) for s, m in zip(stripped_lines, line_midpoint)]

zdnabert_res = zdnabert_res[["Start", "End"]]

zdnabert_res['Chromosome'] = "chr18"

zdnabert_pr = pr.PyRanges(zdnabert_res).merge_overlaps()

zhunt_res = pd.read_csv(
    base_path / "z_dna" / "zhunt" / "run_1" / "clean_chr18.fa.Z-SCORE",
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

def venn_bp(a, b, c):
    def bp(gr): 
        size = int(gr.lengths().sum()) if len(gr) else 0
        size = round(size / 1000, 2)
        return size

    regions = {
        '100': a.subtract_overlaps(b).subtract_overlaps(c).merge_overlaps(),
        '010': b.subtract_overlaps(a).subtract_overlaps(c).merge_overlaps(),
        '110': a.intersect_overlaps(b).subtract_overlaps(c).merge_overlaps(),
        '001': c.subtract_overlaps(a).subtract_overlaps(b).merge_overlaps(),
        '101': a.intersect_overlaps(c).subtract_overlaps(b).merge_overlaps(),
        '011': b.intersect_overlaps(c).subtract_overlaps(a).merge_overlaps(),
        '111': a.intersect_overlaps(b).intersect_overlaps(c).merge_overlaps(),
    }
    order = ['100','010','110','001','101','011','111']
    return tuple(bp(regions[k]) for k in order)

z_dna_venn_data = venn_bp(zseeker_pr, zhunt_pr, zdnabert_pr)

def create_zdna_venn(venn_data):
    fig, ax = plt.subplots(figsize=(3, 3))

    zdna_venn = venn3(
        subsets = venn_data,
        alpha = 0.8,
        set_labels = ('ZSeeker', 'Z-Hunt II', 'Z-DNABERT'),
        set_colors = ("#5E3C4F", "#62979C", "#9C9462")
    )

    zdna_circles = venn3_circles(
        subsets = venn_data,
        linewidth = 1,
        alpha = 1
    )

    for text in zdna_venn.set_labels:
        text.set_fontsize(8)

    for text in zdna_venn.subset_labels:
        text.set_fontsize(6)

    plt.tight_layout()
    plt.savefig(
        base_path / "plots" / "z_dna_venn.pdf",
        transparent = True
    )
    plt.close()

create_zdna_venn(z_dna_venn_data)