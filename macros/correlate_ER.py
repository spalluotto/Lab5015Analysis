#! /usr/bin/env python3
from utils import *
import csv
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)

# paths
# ----------------------------
eos_path = "/eos/home-s/spalluot/MTD/TB_CERN_Sep25/Lab5015Analysis"
inputdir = f"{eos_path}/plots"
outdir_base = "/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep25/ER_studies/"

# arguments
# ----------------------------
parser = argparse.ArgumentParser(description="Energy resolution correlation")
parser.add_argument("-i", "--inputFile", required=True, type=str, help="Input ROOT file")
parser.add_argument("--minEnergy", required=True, type=str, help="minEnergy config file name")
parser.add_argument("-sm", "--sensorModuleID", required=True, type=str, help="Sensor module ID for QAQC ROOT file")
parser.add_argument("--extraLabel", required=False, type=str, default=None, help="Input file has a name like module_{sensor_module_id}_analysis_{extraLabel}. default=None")
parser.add_argument("-o", "--outFolder", required=False, default=None, type=str, help="output folder. default=input name")
args = parser.parse_args()
if args.outFolder == None:
    args.outFolder = args.inputFile
label = args.inputFile
sensor_module_id = args.sensorModuleID
outdir = f"{outdir_base}/{args.outFolder}/"
os.makedirs(outdir, exist_ok=True)
print("Input file:", label)
print("Output folder:", outdir)
colors = cms_colors

# -- min energy values txt
minEnergy_txt = f"{eos_path}/cfg/minEnergies_{args.minEnergy}.txt"
min_energy_dict = read_min_energy(minEnergy_txt)

# -- get QAQC data
LO_dir = "/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_H8_Sep2025/SMs_QAQC/"
if args.extraLabel is not None:
    extra_label = f"_{args.extraLabel}"
else:
    extra_label = ""
f_qaqc = ROOT.TFile.Open(f"{LO_dir}/module_{sensor_module_id}_analysis{extra_label}.root")
g_res = {}
g_res["L"] = f_qaqc.Get("g_lyso_L_peak_res_vs_bar")
g_res["R"] = f_qaqc.Get("g_lyso_R_peak_res_vs_bar")
g_res["L-R"] = f_qaqc.Get("g_avg_lyso_res_vs_bar")

# dict
# ----------------------------
h_energy = {}
mpv_l = {}
res_l = {}
mpv_lg = {}
res_lg = {}
res_lg_gaus = {}
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
f_lg = ROOT.TF1("f_langau", getattr(ROOT,"langaufun"), 0, 1000, 4)
f_lg.SetParNames("Width","MPV","Area","Sigma")


# fit energy histograms 
# ----------------------------    
for key,h in h_energy.items():
    bar, side, vov, thr = key
    h = h_energy[key].Clone()
    f_landau, f_lg, result = fit_landau_langaus(h, min_energy_dict[(bar,vov)], 850)
    mpv_l[(bar,side,vov,thr)] = result["landau_mpv"]
    res_l[(bar,side,vov,thr)] = result["landau_width"]/result["landau_mpv"]
    mpv_lg[(bar,side,vov,thr)] = result["langaus_mpv"]
    res_lg[(bar,side,vov,thr)] = result["langaus_width"]/result["langaus_mpv"]
    res_lg_gaus[(bar,side,vov,thr)] = result["langaus_sigma"]/result["langaus_mpv"]
    
 
# Energy resolution correlation
for vov in Vovs:
    for thr in thresholds:
        c = ROOT.TCanvas(f"c_energy_resolution_correlation_QAQCvsTB_Vov{vov:.2f}_th{thr:02d}","", 600, 500)
        hframe = ROOT.TH2F("hframe","", 10, 0, 0.1, 10, 0.02, 0.15)
        hframe.GetXaxis().SetTitle("Energy resolution TB")
        hframe.GetYaxis().SetTitle("Energy resolution QAQC")
        hframe.Draw()
        g_l = {}
        g_lg = {}
        g_lg_gaus = {}
        for side in sides:
            g_l[side] = ROOT.TGraph()
            g_lg[side] = ROOT.TGraph()
            g_lg_gaus[side] = ROOT.TGraph()
            for i,bar in enumerate(bars):
                key=(bar,side,vov,thr)
                g_l[side].SetPoint(g_l[side].GetN(), res_l[key], g_res[side].Eval(int(bar)))
                g_lg[side].SetPoint(g_lg[side].GetN(), res_lg[key], g_res[side].Eval(int(bar)))
                g_lg_gaus[side].SetPoint(g_lg_gaus[side].GetN(), res_lg_gaus[key], g_res[side].Eval(int(bar)))
            if "L" == side:
                g_l[side].SetMarkerColor(2)
                g_lg[side].SetMarkerColor(2)
                g_lg_gaus[side].SetMarkerColor(2)
            elif "R" == side:
                g_l[side].SetMarkerColor(4)
                g_lg[side].SetMarkerColor(4)
                g_lg_gaus[side].SetMarkerColor(4)
            elif "L-R" == side:
                g_l[side].SetMarkerColor(1)
                g_lg[side].SetMarkerColor(1)
                g_lg_gaus[side].SetMarkerColor(1)
            g_l[side].SetMarkerStyle(20)
            g_lg[side].SetMarkerStyle(24)
            g_lg_gaus[side].SetMarkerStyle(20)
            #g_l[side].Draw("P SAME")
            #g_lg[side].Draw("P SAME")
            g_lg_gaus[side].Draw("P SAME")
            leg = ROOT.TLegend(0.45,0.65,0.88,0.88)
            leg.SetBorderSize(0)
            leg.SetFillStyle(0)
            leg.AddEntry(g_l[side],"Landau Width/MPV","p")
            leg.AddEntry(g_lg_gaus[side],"Langaus (#sigma_{G}/MPV)","p")
            leg.AddEntry(g_lg[side],"Langaus (FWHM/MPV)","p")
            #leg.Draw()
        c.SaveAs(f"{outdir}/energy_resolution_correlation_QAQCvsTB_Vov{vov:.2f}_th{thr:02d}.png")
        del g_l
        del g_lg
        del g_lg_gaus
        del hframe
        
# - tres correlation with energy resolution
filename = f"{inputdir}/summaryPlots_{label}.root"
print("Opening:", filename)
f = ROOT.TFile.Open(filename)
if not f or f.IsZombie():
    print("Cannot open file ", filename)
    sys.exit()
g_tres = {}
g_tres_vs_er = {}
vov = Vovs[0]
thr = 10
graph_name = f"g_deltaT_totRatioCorr_vs_bar__Vov{vov:.2f}_th{thr:02d}"
g_tres = f.Get(graph_name)
g_tres_vs_er = ROOT.TGraph()
c = ROOT.TCanvas(f"c_tres_vs_energy_resolution_Vov{vov:.2f}_th{thr:02d}","", 600, 500)
c.cd()
for bar in range(g_tres.GetN()):
    g_tres_vs_er.SetPoint(g_tres_vs_er.GetN(), g_res["L-R"].Eval(int(bar)), g_tres.Eval(int(bar)))
    print("x ", g_res["L-R"].Eval(int(bar)), "  y ", g_tres.Eval(int(bar)))
g_tres_vs_er.SetMarkerColor(4)
g_tres_vs_er.SetMarkerStyle(20)
g_tres_vs_er.GetYaxis().SetRangeUser(20, 50)
g_tres_vs_er.GetXaxis().SetRangeUser(0.02, 0.15)
g_tres_vs_er.GetXaxis().SetTitle("Energy resolution")
g_tres_vs_er.GetYaxis().SetTitle("#sigma_{t} [ps]")
g_tres_vs_er.Draw("AP")
f = ROOT.TF1("", "pol1")
g_tres_vs_er.Fit(f,"QS")
f.SetLineColor(2)
f.Draw("same")
leg_fit = ROOT.TLegend(0.35,0.65,0.88,0.88)
leg_fit.SetBorderSize(0)
leg_fit.SetFillStyle(0)
#leg_fit.AddEntry(f, f"pol1 - p0 = {f.GetParameter(0):.0f} p1 = {f.GetParameter(1):.2f}","l")
leg_fit.Draw()
c.SaveAs(f"{outdir}/tres_vs_energy_resolution_Vov{vov:.2f}_th{thr:02d}.png")

remove_useless_dirs(outdir)
