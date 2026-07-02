import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fsize = 22
tick_size = 18

dm = {
    "9001" : [33.7608, 31.6392, 30.4032, 27.884, 29.1516, 29.2742, 29.3106, 27.1104, 27.7983, 28.4243, 30.0891, 29.3959, 32.2497, 31.2093, 30.9873, 34.3772],
    "9000" : [33.2457, 31.5417, 30.7123, 30.687, 29.0857, 28.9459, 29.9012, 29.074, 29.9042, 28.3576, 31.5272, 30.3022, 30.4894, 30.6531, 31.781, 33.1243],
    "9005" : [30.4445, 31.9715, 30.8398, 30.693, 30.1605, 29.8004, 28.5805, 30.3734, 30.6305, 28.886, 30.1636, 31.2088, 31.475, 30.2317, 31.6581, 32.567],
    "FE_4587" : [31.3033, 31.5171, 29.8797, 28.6355, 26.7881, 27.5626, 27.4332, 27.683, 27.872, 28.4059, 28.9689, 29.5674, 30.1509, 29.7557, 30.6913, 33.0048]
}

colors = plt.get_cmap('tab20').colors[:16]

# parser
parser = argparse.ArgumentParser(description="Plot da CSV")
parser.add_argument("-i", "--csv_file", required=True, help="Input CSV file")
parser.add_argument("-k", "--key", required=True, type=str, help="DM ID")
args   = parser.parse_args()
key = args.key
input_file = f"/eos/home-s/spalluot/MTD/TB_CERN_Sep25/Lab5015Analysis/plots/moduleCharacterization_step2_{args.csv_file}.csv"
plotdir    = f"/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep25/ModuleCharacterization/{args.csv_file}/triangolo/"
os.makedirs(plotdir, exist_ok=True)

# sigma diff vs bar
def draw_sigma_vs_bar(df, labels, plotname, plot_labels=None):
    if plot_labels is None:
        plot_labels = labels
    plt.figure()
    for i,label in enumerate(labels):
        plt.plot(df["bar"], df[label], label=plot_labels[i])
    plt.xlabel("Bar", fontsize=fsize)
    plt.ylabel(r'$\sigma$ [ps]', fontsize=fsize)
    plt.xticks(fontsize=tick_size)
    plt.yticks(fontsize=tick_size)
    plt.ylim(0, 100)
    plt.legend()
    plt.grid()
    plt.savefig(f"{plotdir}/{plotname}.png")

# time walk slope vs bar
def draw_TWslope_vs_bar(df, plotname, ref=False):
    plt.figure()
    if ref:
        ext = "_ref"
    else:
        ext = ""
    plt.plot(df["bar"], df[f"slopeL{ext}"], label="left")
    plt.plot(df["bar"], df[f"slopeR{ext}"], label="right")
    plt.xlabel("Bar", fontsize=fsize)
    plt.ylabel("TW slope", fontsize=fsize)
    plt.xticks(fontsize=tick_size)
    plt.yticks(fontsize=tick_size)
    plt.legend()
    plt.grid()
    plt.ylim(-1.3, -0.5)
    plt.tight_layout()
    plt.savefig(f"{plotdir}/{plotname}.png", dpi=300)
    plt.close()

def draw_TWslope_vs_bar_mpv(df, plotname, ref=False):
    if ref:
        ext = "_ref"
    else:
        ext = ""
    plt.figure(figsize=(12, 10))
    sc = plt.scatter( df["bar"], df[f"slopeL{ext}"], c=df["mpvL"], cmap="viridis", s=100,)
    plt.xlabel("Bar", fontsize=fsize)
    plt.ylabel("TW slope left", fontsize=fsize)
    plt.title("Left", fontsize=fsize)
    plt.xticks(fontsize=tick_size)
    plt.yticks(fontsize=tick_size)
    plt.ylim(-1.3, -0.5)
    plt.grid()
    cbar = plt.colorbar(sc)
    cbar.set_label("MPV left", fontsize=fsize)
    plt.tight_layout()
    plt.savefig(f"{plotdir}/{plotname}_left.png", dpi=300)
    plt.close()

    plt.figure(figsize=(12, 10))
    sc = plt.scatter( df["bar"], df[f"slopeR{ext}"], c=df["mpvR"],cmap="viridis", s=100,)
    plt.xlabel("Bar", fontsize=fsize)
    plt.ylabel("TW slope right", fontsize=fsize)
    plt.title("Right", fontsize=fsize)
    plt.xticks(fontsize=tick_size)
    plt.yticks(fontsize=tick_size)
    plt.ylim(-1.3, -0.5)
    plt.grid()
    cbar = plt.colorbar(sc)
    cbar.set_label("MPV right", fontsize=fsize)
    plt.tight_layout()
    plt.savefig(f"{plotdir}/{plotname}_right.png", dpi=300)
    plt.close()
    
def draw_TW(df, plotname, ref=False, aligned=False):
    x = np.linspace(100, 600, 60)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharex=True)
    axL, axR = axes
    ext = "_ref" if ref else ""
    j = 0
    for i, row in df.iterrows():
        color = colors[j%16]
        if aligned:
            offL, offR = 0, 0
        else:
            offL = row[f"offsetL{ext}"]
            offR = row[f"offsetR{ext}"]
        axL.plot(x, row[f"slopeL{ext}"] * x + offL, alpha=0.7, label=f"Bar {i}", color=color)
        axR.plot(x, row[f"slopeR{ext}"] * x + offR, alpha=0.7, label=f"Bar {i}", color=color)
        j = j+1
    axL.set_xlim(100, 600)
    axR.set_xlim(100, 600)
    axL.set_xlabel("Energy [ADC]", fontsize=fsize)
    axR.set_xlabel("Energy [ADC]", fontsize=fsize)
    axL.set_ylabel("Time [ps]", fontsize=fsize)
    axL.set_title("Left", fontsize=fsize)
    axR.set_title("Right", fontsize=fsize)
    axL.legend(fontsize=8)
    axR.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(f"{plotdir}/{plotname}.png", dpi=300)
    plt.close()

df = pd.read_csv(input_file)
print(df)
# define new columns
df["bar"] = df["index"] % 100

df["sigmaAve_ch"] = np.sqrt(np.maximum(0, df["sigmaDutRef"]**2 - df["sigmaRef"]**2))*np.sqrt(2)
df["sigmaAve_bar"] = np.sqrt(np.maximum(0, df["sigmaDutRef"]**2 - df["sigmaRef"]**2))

df["sigmaRef_ch"] = df["sigmaRef"]*np.sqrt(2)

df["sigmaDiff_ch"] = df["sigmaLR"]/np.sqrt(2)
df["sigmaDiff_bar"] = df["sigmaLR"]/2

ref = df["sigmaRef"].mean()
ref_err = df["sigmaRef"].std(ddof=1) / np.sqrt(len(df))

df["sigmaDiff_bar_moduleChar"] = dm[key]


df["sigmaAve_ch__RefAvgOverBars"] = np.sqrt(np.maximum(0, df["sigmaDutRef"]**2 - ref**2))*np.sqrt(2)
df["sigmaAve_bar__RefAvgOverBars"] = np.sqrt(np.maximum(0, df["sigmaDutRef"]**2 - ref**2))

draw_sigma_vs_bar(df, ["sigmaLRef", "sigmaRRef", "sigmaLR"], "triangolo_sigma_deltaT_vs_bar")
draw_sigma_vs_bar(df, ["sigmaL", "sigmaR", "sigmaRef"], "triangolo_sigma_t_vs_bar")
draw_sigma_vs_bar(df, ["sigmaL", "sigmaR", "sigmaAve_ch", "sigmaDiff_ch", "sigmaRef_ch"], "sigma_ch_vs_bar", plot_labels=["L da triangolo", "R da triangolo", "ch da Ave-Ref", "ch da L-R", "REF ch da triangolo"])

draw_sigma_vs_bar(df, ["sigmaAve_bar", "sigmaDiff_bar"], "sigma_diff_vs_average", plot_labels=["average", "difference"])
draw_sigma_vs_bar(df, ["sigmaAve_bar__RefAvgOverBars", "sigmaDiff_bar"], "sigma_diff_vs_average__RefAvgOverBars", plot_labels=["average", "difference"])
draw_sigma_vs_bar(df, ["sigmaAve_bar", "sigmaDiff_bar", "sigmaDiff_bar_moduleChar"], "sigma_diff_vs_average__comparisonModuleChar", plot_labels=["average", "difference", "difference moduleChar"])


# # time walk 
draw_TWslope_vs_bar(df, "time_walk_slope_vs_bar_REF", ref=True)
draw_TWslope_vs_bar(df, "time_walk_slope_vs_bar_DUT", ref=False)
draw_TW(df,  "time_walk_vs_energy_REF_aligned", ref=True, aligned=True)
draw_TW(df,  "time_walk_vs_energy_DUT_aligned", ref=False, aligned=True)
draw_TWslope_vs_bar_mpv(df, "timw_walk_slope_mpv_vs_bar_DUT", ref=False)
draw_TWslope_vs_bar_mpv(df, "timw_walk_slope_mpv_vs_bar_REF", ref=True)
