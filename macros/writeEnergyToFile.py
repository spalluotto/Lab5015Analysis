#! /usr/bin/env python3
from utils import *

# paths
# ----------------------------
eos_path = "/eos/home-s/spalluot/MTD/TB_CERN_Sep25/Lab5015Analysis"
inputdir = f"{eos_path}/plots"

# arguments
# ----------------------------
parser = argparse.ArgumentParser(description="Energy spectra comparison")
parser.add_argument("-i", "--inputLabels", required=True, type=str, help="comma separated labels")
args = parser.parse_args()
label_list = args.inputLabels.split(",")
short_label_list = []
print("Input labels:", label_list)

# read histograms
# ----------------------------
for label in label_list:
    filename = f"{inputdir}/moduleCharacterization_step2_{label}.root"
    print("Opening:", filename)
    f = ROOT.TFile.Open(filename)
    if not f or f.IsZombie():
        print("Cannot open file")
        continue
    outfile = ROOT.TFile(f"{inputdir}/energy_spectra_{label}.root", "RECREATE")
    for key in f.GetListOfKeys():
        name = key.GetName() # e.g. h1_energy_bar05L_Vov2.50_th11
        if not name.startswith("h1_energy_bar"):
            continue
        h = f.Get(name)
        if not h:
            continue
        h_clone = h.Clone()
        h_clone.SetDirectory(0)
        outfile.cd()
        h_clone.Write()
    outfile.Close()
    f.Close()


