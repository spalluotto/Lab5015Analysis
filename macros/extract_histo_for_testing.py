#!/usr/bin/env python3
import ROOT
infile = ROOT.TFile.Open("../plots/moduleCharacterization_step1_DM_9001_Vov3.00_T18C_refBar0.root")
outfile = ROOT.TFile("test_histos.root", "RECREATE")
keys = infile.GetListOfKeys()
selected = []
for key in keys:
    name = key.GetName()
    if "h1_energy" in name and "th10" in name and "bar05L_V" in name:
        print("Taking:", name)
        h = key.ReadObj()
        h.SetDirectory(0)
        selected.append(h)

outfile.cd()
for h in selected:
    h.Write()
outfile.Close()
infile.Close()
print(f"\nSaved {len(selected)} histograms in test_histos.root")
