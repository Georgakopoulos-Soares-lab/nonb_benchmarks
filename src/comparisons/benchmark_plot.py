import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt
from pathlib import Path

base_dir = Path("../..")
benchmarks = base_dir / "benchmarks"
plots = base_dir / "results" / "plots"

plots.mkdir(parents=True, exist_ok=True)

def read_benchmark(benchmark_path):
    with open(benchmark_path) as f:
        for line in f:
            split_line = line.rstrip("\n").split(":")
            if split_line[0] == "\tUser time (seconds)":
                time = float(split_line[1])
            elif split_line[0] == "\tMaximum resident set size (kbytes)":
                memory = float(split_line[1]) / 1_048_576.0

    return time, memory

rows = []
for nonb_dir in (benchmarks).iterdir():
    if nonb_dir.name == ".DS_Store":
        continue
    for tool_dir in nonb_dir.iterdir():
        if tool_dir.name == ".DS_Store":
            continue
        for iteration in tool_dir.iterdir():
            if iteration.name == ".DS_Store":
                continue
            time, memory = read_benchmark(iteration)
            rows.append({
                "nonb": nonb_dir.name,
                "tool": tool_dir.name,
                "time": time,
                "memory": memory,
            })

benchmarks_res = pd.DataFrame(rows)

nonb_dict = {
    "dr_and_str": "DRs & STRs",
    "g4": "G4s",
    "h_dna": "H-DNA",
    "ir": "IRs",
    "r_loops": "R-loops",
    "z_dna": "Z-DNA",
    "general": "General prediction"
}

benchmarks_res["nonb"] = benchmarks_res["nonb"].map(nonb_dict)

nonb_palette = {
    "DRs & STRs": "#5B4289",
    "G4s": "#798CB1",
    "H-DNA": "#95B4C2",
    "IRs": "#CFC3BB",
    "R-loops": "#A77668",
    "Z-DNA": "#6B324F"
}

nonb_order = list(nonb_palette)

tool_order = (
    benchmarks_res
    .groupby(["nonb", "tool"], observed=True)["time"].mean()
    .reset_index()
    .assign(rank=lambda d: d["nonb"].map({k: i for i, k in enumerate(nonb_order)}))
    .sort_values(["rank", "time"])
    ["tool"].tolist()
)

fig, axes = plt.subplots(1, 2, figsize = (8, 6), sharey = True, layout = "constrained")

common = dict(
    data=benchmarks_res,
    hue="nonb",
    orient="h",
    y="tool",
    order=tool_order,
    hue_order=nonb_order,
    palette=nonb_palette,
    zorder=10,
    errorbar="sd",
    edgecolor="black",
    linewidth=1,
)

sns.barplot(x = "time", ax = axes[0], **common)
axes[0].set_xscale("log")
axes[0].set_xlabel(r"Time (log$_{10}$ seconds")
axes[0].set_ylabel("Non-B DNA prediction algorithm")

sns.barplot(x = "memory", ax = axes[1], legend = False, **common)
axes[1].set_xlabel(r"Peak memory usage (log$_{10}$ GB)")
axes[1].set_xscale("log")
axes[1].set_ylabel("")

for ax in axes:
    ax.grid(zorder=1)
    plt.setp(ax.patches, edgecolor="black", linewidth=1)

handles, labels = axes[0].get_legend_handles_labels()
axes[0].get_legend().remove()

fig.legend(
    handles, labels,
    loc = "outside lower center",
    ncols = len(labels),
    frameon = False,
    fontsize = 8
)

sns.despine()
fig.savefig(
    plots / "benchmark_plot.pdf",
    transparent = True
)

benchmarks_res = benchmarks_res.rename(
    columns={
        "nonb": "Non-B DNA class",
        "tool": "Tool",
        "time": "Time (seconds)",
        "memory": "Peak memory (GB)"
    }
)

benchmarks_res['Time (hours)'] = benchmarks_res['Time (seconds)'] / 3600
benchmarks_res['Time (hours)'] = round(benchmarks_res['Time (hours)'], 2)
benchmarks_res['Time (seconds)'] = round(benchmarks_res['Time (seconds)'], 2)
benchmarks_res['Peak memory (GB)'] = round(benchmarks_res['Peak memory (GB)'], 2)

benchmarks_res.to_csv(
    base_dir / "results" / 'performance_benchmarks.csv',
    index=False
)