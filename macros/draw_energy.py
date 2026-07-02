#! /usr/bin/env python3
from utils import *
import csv
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
colors = [
    ROOT.kRed+1,
    ROOT.kBlue+1,
    ROOT.kGreen+2,
    ROOT.kMagenta+1,
    ROOT.kOrange+7,
    ROOT.kCyan+2,
    ROOT.kViolet+1,
    ROOT.kAzure+2,
    ROOT.kPink+7,
    ROOT.kSpring+5,
    ROOT.kTeal+3,
    ROOT.kYellow+2,
    ROOT.kGray+2,
    ROOT.kRed-7,
    ROOT.kBlue-7,
    ROOT.kGreen-7
]
# paths
# ----------------------------
eos_path = "/eos/home-s/spalluot/MTD/TB_CERN_Sep25/Lab5015Analysis"
inputdir = f"{eos_path}/plots"
outdir_base = "/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep25/ER_studies/"

# arguments
# ----------------------------
parser = argparse.ArgumentParser(description="Energy spectra comparison")
parser.add_argument("-i", "--inputFile", required=True, type=str, help="Input ROOT file")
parser.add_argument("-b", "--bars", required=True, type=str, help="Bars you want to compare")
parser.add_argument("-o", "--outFolder", required=False, default=None, type=str, help="output folder. default=input name")
args = parser.parse_args()
if args.outFolder == None:
    args.outFolder = args.inputFile
label = args.inputFile
bars_toComp = [int(x) for x in args.bars.split(',')]
outdir = f"{outdir_base}/{args.outFolder}/"
os.makedirs(outdir, exist_ok=True)
print("Input file:", label)
print("Output folder:", outdir)

# dict
# ----------------------------
h_energy = {}
bars = set()
Vovs = set()
thresholds = set()
sides = set()

# read histograms
# ----------------------------
filename = f"{inputdir}/moduleCharacterization_step1_{label}.root"
print("Opening:", filename)
f = ROOT.TFile.Open(filename)
if not f or f.IsZombie():
    print("Cannot open file")
    sys.exit()
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
    h_energy[(bar, side, vov, thr)] = h_clone
    h_energy[(bar, side, vov, thr)].SetDirectory(0)        
f.Close()
bars = sorted(bars)
Vovs = sorted(Vovs)
thresholds = sorted(thresholds)
sides = sorted(sides)
print("bars:", bars)
print("Vovs:", Vovs)
print("thresholds:", thresholds)


print("\nDraw in same canvas")
# draw histo same canvas
# ----------------------------    
h = {}
for vov in Vovs:
    for thr in thresholds:
        for side in sides:
            c = ROOT.TCanvas(f"c_energy_{side}_Vov{vov:.2f}_th{thr:02d}", "", 600, 500)
            hframe = ROOT.TH2F("hframe","", 10, 0, 900, 10, 0, 1.2)
            hframe.GetXaxis().SetTitle("Energy")
            hframe.GetYaxis().SetTitle("Entries")
            hframe.Draw()
            leg = ROOT.TLegend(0.60,0.45,0.88,0.88)
            leg.SetBorderSize(0)
            leg.SetFillStyle(0)
            j=0
            for i,bar in enumerate(bars_toComp):
                key=(bar,side,vov,thr)
                if key not in h_energy:
                    print(f"Warning: {key} missing!")
                    continue
                h[key] = h_energy[key].Clone()
                h[key].SetDirectory(0)
                integral = h[key].Integral()
                # print("integral ", integral)
                # rebin = get_rebin_factor(integral)
                rebin = 8
                h[key].Rebin(rebin)                
                bin_min = h[key].GetXaxis().FindBin(50)
                bin_max = h[key].GetXaxis().FindBin(850)
                max_bin = max(range(bin_min, bin_max+1), key=lambda b: h[key].GetBinContent(b))
                max_content = h[key].GetBinContent(max_bin)
                h[key].Scale(1/max_content)
                h[key].SetLineColor(colors[j % len(colors)])
                h[key].SetLineWidth(1)
                leg.AddEntry(h[key], f"Bar {bar}", "l")
                j = j+1
                h[key].Draw("hist same")
            outfile = (f"{outdir}/compare_h_energy_{side}_Vov{vov:.2f}_th{thr:02d}.png")
            leg.Draw()
            c.SaveAs(outfile)
            del c
            del hframe
del h
remove_useless_dirs(outdir)
