from utils import *
import re
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)

# paths
# ----------------------------
eos_path = "/eos/home-s/spalluot/MTD/TB_CERN_Sep25/Lab5015Analysis"
inputdir = f"{eos_path}/plots"
outdir_base = "/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep25/ER_studies/"

print("[REMINDER] hard-code: vov=3.00")

# arguments
# ----------------------------
parser = argparse.ArgumentParser(description="Energy spectra comparison")
parser.add_argument("-i", "--inputLabels", required=True, type=str, help="comma separated list of files")
parser.add_argument("-o", "--outFolder", required=True, type=str, help="output folder")
parser.add_argument("-th", "--threshold", required=True, type=int, help="threshold")
args = parser.parse_args()
label_list = args.inputLabels.split(",")
label_to_pos = {}
for raw in label_list:
    match = re.search(r"refBar(\d+)", raw)
    if match:
        label_to_pos[raw] = int(match.group(1))
outdir = f"{outdir_base}/{args.outFolder}/"
os.makedirs(outdir, exist_ok=True)
print("Input labels:", label_list)
print("Output folder:", outdir)

vov = 3
thr = args.threshold
graph_name = f"g_deltaT_totRatioCorr_vs_bar__Vov{vov:.2f}_th{thr:02d}"

graphs = {}
for label in label_list:
    filename = f"{inputdir}/summaryPlots_{label}.root"
    print("Opening:", filename)
    f = ROOT.TFile.Open(filename)
    if not f or f.IsZombie():
        print("Cannot open file")
        continue
    graphs[label] = f.Get(graph_name)
        
g = {}
for bar in range(16):
    c = ROOT.TCanvas(f"c_tres_vs_pos_bar{bar:02d}_Vov{vov:.2f}_th{thr:02d}","", 600, 500)
    hframe = ROOT.TH2F("hframe","", 10, 25, 55, 10, 10, 60)
    hframe.GetXaxis().SetTitle("x [mm]")
    hframe.GetYaxis().SetTitle("#sigma_{t} [ps]")
    hframe.Draw()
    g[bar] = ROOT.TGraph()
    for i,label in enumerate(label_list):        
        x_position = 3.12*label_to_pos[label]/math.cos(math.radians(52))
        g[bar].SetPoint(g[bar].GetN(), x_position, graphs[label].Eval(int(bar)))
    g[bar].SetMarkerColor(4)
    g[bar].SetMarkerStyle(20)
    g[bar].Draw("P SAME")
    f = ROOT.TF1("", "pol1")
    g[bar].Fit(f,"QS")
    f.SetLineColor(2)
    f.Draw("same")
    leg_fit = ROOT.TLegend(0.35,0.65,0.88,0.88)
    leg_fit.SetBorderSize(0)
    leg_fit.SetFillStyle(0)
    leg_fit.AddEntry(f, f"pol1 - p0 = {f.GetParameter(0):.0f} p1 = {f.GetParameter(1):.2f}","l")
    leg_fit.Draw()
    c.SaveAs(f"{outdir}/tres_vs_pos_bar{bar:02d}_Vov{vov:.2f}_th{thr:02d}.png")
    del hframe
    del c
    del f
