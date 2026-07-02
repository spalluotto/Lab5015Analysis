#!/usr/bin/env python3
import os
import sys
import argparse
import ROOT
from utils import *

# ---- settings ----------
EOS_PATH = "/eos/home-s/spalluot/MTD/TB_CERN_Sep25/Lab5015Analysis/"
BASE_OUTDIR = "/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep25/ModuleCharacterization/"
SOURCE = "TB"

parser = argparse.ArgumentParser(description="Module characterization summary plots")
parser.add_argument("-i", "--inputLabels", required=True, type=str)
parser.add_argument("-m", "--resMode", default=2, type=int)
parser.add_argument("-o", "--outFolder", type=str)
parser.add_argument("-minEn", "--minEnergyFile", default=None, type=str)
args = parser.parse_args()

# ------------------ 
# -- functions
def open_root(path):
    f = ROOT.TFile.Open(path)
    if not f or f.IsZombie():
        raise IOError(f"Invalid ROOT file: {path}")
    return f

def init_graphs(vovs):
    return {v: ROOT.TGraphErrors() for v in vovs}

def shift_graph_to_zero_mean(g, mean):
    n = g.GetN()
    for i in range(n):
        g.SetPoint(i, g.GetX()[i], g.GetY()[i] - mean)
# ------------------ 
labels = args.inputLabels.split(",")
if args.outFolder:
    outFolder = args.outFolder
elif len(labels) == 1:
    outFolder = labels[0]
else:
    sys.exit("[ERROR] Multiple labels but no output folder specified")

inputdir = f"{EOS_PATH}/plots/"
outdir = os.path.join(BASE_OUTDIR, outFolder)
outdir = f"{outdir}/summaryPlots/offset/"
os.makedirs(outdir, exist_ok=True)
outfile = ROOT.TFile( f"{inputdir}/offset_{outFolder}.root", "RECREATE" )

# TB-only setup (fixed)
enBins = [1]

print("\nGetting tokens from step2: ")
# - Get list of bars, Vovs, thresholds from the step2 file
bars = []
thresholds = []
Vovs = [] 
for label in labels:
    inputFile = open_root(f"{inputdir}/moduleCharacterization_step2_{label}.root")
    listOfKeys = [key.GetName().replace('h1_deltaT_totRatioCorr_','') for key in ROOT.gDirectory.GetListOfKeys() if key.GetName().startswith('h1_deltaT_totRatioCorr_bar')]
    for k in listOfKeys:
        barNum = int (k.split('_')[0][3:5])
        bars.append(barNum)
        vov = float (k.split('_')[1][3:7])
        Vovs.append(vov)
        thr = int (k.split('_')[2][2:4])
        thresholds.append(thr)
# - remove duplicates
bars = [i for n, i in enumerate(bars) if i not in bars[:n]]
Vovs = [i for n, i in enumerate(Vovs) if i not in Vovs[:n]]
thresholds = [i for n, i in enumerate(thresholds) if i not in thresholds[:n]]
bars.sort()
Vovs.sort()
thresholds.sort()
VovsEff = {v: Vovs_eff(outFolder, v) for v in Vovs}
goodBars = good_bars(outFolder, VovsEff, bars)
print(' - bars:', bars)
print(' - good bars:', goodBars)
print(' - Vovs:',Vovs)
print(' - thresholds:', thresholds)

# create graphs
graphs = {(v, 1): ROOT.TGraphErrors() for v in Vovs}

# loop over files
for label in labels:
    print(f"\nProcessing {label}")
    f = open_root(f"{inputdir}/moduleCharacterization_step2_{label}.root")

    # best resolution per bar/vov
    best = {}
    for bar in bars:
        for vov in Vovs:
            best[(bar, vov)] = [9999, 9999]
    for bar in bars:
        for vov in Vovs:
            if bar not in goodBars[vov]:
                continue
            for thr in thresholds:
                hname = f"h1_deltaT_energyRatioPhaseCorr_bar{bar:02d}L-R_Vov{vov:.02f}_th{thr:02d}_energyBin01"
                h = f.Get(hname)
                if not isinstance(h, ROOT.TH1F):
                    continue
                if h.GetEntries() < 200:
                    continue
                res = getTimeResolution(h)
                if res[0] < best[(bar, vov)][0]:
                    best[(bar, vov)] = res
    # fill graphs
    for bar in bars:
        for vov in Vovs:
            res = best[(bar, vov)]
            if res[0] == 9999:
                continue
            g = graphs[(vov, 1)]
            n = g.GetN()
            g.SetPoint(n, bar, res[2])
            g.SetPointError(n, 0, res[3])

c = ROOT.TCanvas("c_mean_deltaT_vs_bar")
frame = ROOT.TH2F("", "", 100, -0.5, 15.5, 100, -1000, 1000)
frame.SetTitle("; bar; #mu_{#DeltaT} [ps]")
frame.Draw()
leg = ROOT.TLegend(0.15, 0.7, 0.85, 0.9)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
colors = cms_colors
for i, vov in enumerate(Vovs):
    g = graphs[(vov, 1)]
    g.SetMarkerStyle(20+i)
    g.SetMarkerColor(colors[i % len(colors)])
    g.SetLineColor(colors[i % len(colors)])
    fit = ROOT.TF1(f"fit_{vov}", "pol0", 0, 16)
    g.Fit(fit, "QRN")
    print(f"Vov {vov:.2f} V \t mean {fit.GetParameter(0):.0f} \t RMS {g.GetRMS(2):.0f}")
    shift_graph_to_zero_mean(g, fit.GetParameter(0))
    g.Draw("PL SAME")
    leg.AddEntry(g, f"Vov {vov:.2f}V | #mu = {fit.GetParameter(0):.0f} ps | RMS = {g.GetRMS(2):.0f}", "PL")
    outfile.cd()
    g.Write(f"g_mean_Vov{vov:.2f}")
leg.Draw()
c.SaveAs(f"{outdir}/{c.GetName()}.png")
outfile.Close()

