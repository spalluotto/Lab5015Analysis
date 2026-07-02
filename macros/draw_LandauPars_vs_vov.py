#! /usr/bin/env python3
from utils import *
import csv
import re
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)

# paths
# ----------------------------
eos_path = "/eos/home-s/spalluot/MTD/TB_CERN_Sep25/Lab5015Analysis"
inputdir = f"{eos_path}/plots"
outdir_base = "/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep25/ER_studies/"


# arguments
# ----------------------------
parser = argparse.ArgumentParser(description="Energy spectra comparison")
parser.add_argument("-i", "--inputLabels", required=True, type=str, help="comma separated list of files")
parser.add_argument("-o", "--outFolder", required=True, type=str, help="output folder. default=input name")
parser.add_argument("--minEnergy", required=True, type=str, help="minEnergy config file name")
args = parser.parse_args()
label_list = args.inputLabels.split(",")
label_to_vov = {}
for label in label_list:
    match = re.search(r"Vov([0-9]+\.?[0-9]*)", label)
    if match:
        label_to_vov[label] = float(match.group(1))
    else:
        raise ValueError(f"Vov not found: {label}")
outdir = f"{outdir_base}/{args.outFolder}/"
os.makedirs(outdir, exist_ok=True)
print("Input labels:", label_list)
print("Output folder:", outdir)
colors = cms_colors

# min energy values
minEnergy_txt = f"{eos_path}/cfg/minEnergies_{args.minEnergy}.txt"
min_energy_dict = read_min_energy(minEnergy_txt)


# dict
# ----------------------------
h_energy = {}
mpv_l = {}
mpv_lg = {}
bars = set()
Vovs = set()
thresholds = set()
sides = set()

# read histograms
# ----------------------------
for label in label_list:
    filename = f"{inputdir}/moduleCharacterization_step1_{label}.root"
    print("Opening:", filename)
    f = ROOT.TFile.Open(filename)
    if not f or f.IsZombie():
        print("Cannot open file")
        continue
    for key in f.GetListOfKeys():
        name = key.GetName()
        if not name.startswith("h1_energy_bar"):
            continue
        # decode info from the energy histogram name
        parts = name.split("_")
        bar = int(parts[2][3:5])
        side = parts[2][5:]  # L or R
        vov = float(parts[3][3:])
        thr = int(parts[4][2:])
        bars.add(bar)
        Vovs.add(vov)
        thresholds.add(thr)
        sides.add(side)
        h = f.Get(name)
        if not h:
            continue
        h_clone = h.Clone()
        h_clone.SetDirectory(0)
        h_energy[(label, bar, side, vov, thr)] = h_clone
        h_energy[(label, bar, side, vov, thr)].SetDirectory(0)        
    f.Close()
bars = sorted(bars)
Vovs = sorted(Vovs)
thresholds = sorted(thresholds)
sides = sorted(sides)
print("bars:", bars)
print("Vovs:", Vovs)
print("thresholds:", thresholds)

# fit energy histograms 
# ----------------------------    
for key,histo in h_energy.items():
    label,bar, side, vov, thr = key
    h = h_energy[key].Clone()
    if h is None:
        continue
    if h.GetEntries()<20:
        continue
    f_landau, f_lg, result = fit_landau_langaus(h, min_energy_dict[(bar,vov)], 850)
    mpv_l[(label,bar,side,vov,thr)] = result["landau_mpv"]
    mpv_lg[(label,bar,side,vov,thr)] = result["langaus_mpv"]

# MPV vs label plots
sorted_labels=sorted(label_list,key=lambda l:label_to_vov[l])
for thr in thresholds:
    c=ROOT.TCanvas(f"c_mpv_vs_Vov_th{thr:02d}","",600,500)
    hframe=ROOT.TH2F("hframe","",10,0,max(label_to_vov.values())+0.5,10,100,600)
    hframe.GetXaxis().SetTitle("V_{OV} [V]")
    hframe.GetYaxis().SetTitle("Landau MPV")
    hframe.Draw()
    g_l={}
    g_lg={}
    for side in sides:
        g_l[side]=ROOT.TGraph()
        g_lg[side]=ROOT.TGraph()
        for label in sorted_labels:
            vov=label_to_vov[label]
            for bar in bars:
                key=(label,bar,side,vov,thr)
                if key not in mpv_l: continue
                g_l[side].SetPoint(g_l[side].GetN(),vov,mpv_l[key])
                g_lg[side].SetPoint(g_lg[side].GetN(),vov,mpv_lg[key])
    for side in sides:
        color=2 if side=="L" else 4 if side=="R" else 1
        g_l[side].SetMarkerColor(color)
        g_lg[side].SetMarkerColor(color)
        g_l[side].SetMarkerStyle(20)
        g_lg[side].SetMarkerStyle(24)
        g_l[side].Draw("P SAME")
    c.SaveAs(f"{outdir}/mpv_vs_vov_th{thr:02d}.png")
    del g_l
    del g_lg
    del hframe
