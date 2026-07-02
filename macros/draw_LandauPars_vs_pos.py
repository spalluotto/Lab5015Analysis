#! /usr/bin/env python3
from utils import *
import re
import csv
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)

# paths
# ----------------------------
eos_path = "/eos/home-s/spalluot/MTD/TB_CERN_Sep25/Lab5015Analysis"
inputdir = f"{eos_path}/plots"
outdir_base = "/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep25/ER_studies/"

xmin = 2.5
xmax = 5.5


# arguments
# ----------------------------
parser = argparse.ArgumentParser(description="Energy spectra comparison")
parser.add_argument("-i", "--inputLabels", required=True, type=str, help="comma separated list of files")
parser.add_argument("-o", "--outFolder", required=False, default=None, type=str, help="output folder. default=input name")
parser.add_argument("--minEnergy", required=True, type=str, help="minEnergy config file name")
args = parser.parse_args()
label_list = args.inputLabels.split(",")
label_to_pos = {}
for raw in label_list:
    match = re.search(r"refBar(\d+)", raw)
    if match:
        label_to_pos[raw] = int(match.group(1))
if args.outFolder == None and len(label_list) == 1:
    args.outFolder = args.inputLabels
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
res_l = {}
mpv_lg = {}
mpv_lg_err = {}
res_lg = {}
res_lg_gaus = {}
res_lg_gaus_err = {}
bars = set()
Vovs = set()
thresholds = set()
sides = set()

print(" ---------> Get energy histograms")
# read histograms
# ----------------------------
for label in label_list:
    #filename = f"{inputdir}/energy_calib_TOFHIR_LO_{label}.root"
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
        if h is None:
            continue
        if not isinstance(h, ROOT.TH1F):
            continue
        if h.GetEntries() < 20:
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
f_landau = ROOT.TF1("f_landau","[0]*TMath::Landau(x,[1],[2])",0,1000)
f_lg = ROOT.TF1("f_langau", getattr(ROOT,"langaufun"), 0, 1000, 4)
f_lg.SetParNames("Width","MPV","Area","Sigma")


print(" ---------> Fit energy histograms")
# fit energy histograms 
# ----------------------------    
for key,histo in h_energy.items():
    label,bar, side, vov, thr = key
    if key not in h_energy:
        continue
    h = h_energy[key].Clone()
    f_landau, f_lg, result = fit_landau_langaus(h, min_energy_dict[(bar,vov)], 850)
    if result["landau_mpv"] == 0:
        print("[ERROR] Failed fit, 0 MPV")
        continue
    mpv_l[(label,bar,side,vov,thr)] = result["landau_mpv"]
    res_l[(label,bar,side,vov,thr)] = result["landau_width"]/result["landau_mpv"]
    mpv_lg[(label,bar,side,vov,thr)] = result["langaus_mpv"]
    mpv_lg_err[(label,bar,side,vov,thr)] = result["langaus_mpv_err"]
    res_lg[(label,bar,side,vov,thr)] = result["langaus_width"]/result["langaus_mpv"]
    res_lg_gaus[(label,bar,side,vov,thr)] = result["langaus_sigma"]/result["langaus_mpv"]
    res_lg_gaus_err[(label,bar,side,vov,thr)] = ( res_lg_gaus[(label,bar,side,vov,thr)] * math.sqrt( (result["langaus_sigma_err"] / result["langaus_sigma"])**2 + (result["langaus_mpv_err"] / result["langaus_mpv"])**2))
    if thr == 10:
        c_single = ROOT.TCanvas(f"c_{label}_{bar}_{side}_{vov}_{thr}","",800,600)
        h.SetLineColor(1)
        h.GetXaxis().SetRangeUser(0,850)
        h.Draw("hist")
        f_lg.SetLineColor(ROOT.kRed)
        f_lg.SetLineWidth(2)
        f_lg.Draw("same")
        f_landau.SetLineColor(ROOT.kBlue)
        f_landau.SetLineWidth(2)
        f_landau.Draw("same")
        leg_fit = ROOT.TLegend(0.35,0.65,0.88,0.88)
        leg_fit.SetBorderSize(0)
        leg_fit.SetFillStyle(0)
        leg_fit.AddEntry(f_landau, f"landau - mpv = {f_landau.GetParameter(1):.0f}","l")
        leg_fit.AddEntry(f_lg, f"langaus - mpv = {f_lg.GetParameter(1):.0f}","l")
        leg_fit.Draw()
        outfile_single = (f"{outdir}/h_energy_{label}_bar{bar:02d}{side}_Vov{vov:.2f}_th{thr:02d}.png")
        c_single.SaveAs(outfile_single)

print(" ---------> Plot MPV vs label")
# MPV vs label plots
# -------------------------------
# - compute normalization of energy profiles along impact point position (aka label)
mpv_mean_lr = {}
for bar in bars:
    for vov in Vovs:
        for thr in thresholds:
            vals = []
            for label in label_list:
                for side in ["L", "R"]:
                    key = (label, bar, side, vov, thr)
                    if key in mpv_lg:
                        vals.append(mpv_lg[key])
            if len(vals) > 0:
                mpv_mean_lr[(bar, vov, thr)] = sum(vals) / len(vals)

h_slope_mpv = ROOT.TH1F("", "; Slope energy vs x [cm^{-1}]; Entries", 32, -0.02, 0.1)
h_slope_mpv.SetLineColor(ROOT.kBlue+1)

# - loop over bar vov th label
if len(label_list) > 1:
        for bar in bars:
            for vov in Vovs:
                for thr in thresholds:
                    c = ROOT.TCanvas(f"c_mpv_vs_pos_{bar:02d}_Vov{vov:.2f}_th{thr:02d}","", 600, 500)
                    hframe = ROOT.TH2F("hframe","", 10, xmin, xmax, 10, 0.8, 1.2)
                    hframe.GetXaxis().SetTitle("x [cm]")
                    hframe.GetYaxis().SetTitle("Normalized energy")
                    hframe.Draw()
                    g_l = {}
                    g_lg = {}
                    latex = ROOT.TLatex()
                    latex.SetNDC(True)
                    latex.SetTextSize(0.035)
                    latex.SetTextFont(42)
                    fit_results = {}
                    for j,side in enumerate(sides):
                        g_l[side] = ROOT.TGraph()
                        g_lg[side] = ROOT.TGraphErrors()
                        fit_name = f"f_pol1_{side}_{bar}_{vov}_{thr}"
                        f_pol1 = ROOT.TF1(fit_name, "pol1", xmin, xmax)
                        for i,label in enumerate(label_list):
                            key=(label,bar,side,vov,thr)
                            if key not in mpv_l:
                                continue
                            x_position = 3.12*label_to_pos[label]/math.cos(math.radians(52))/10
                            g_l[side].SetPoint(g_l[side].GetN(), x_position, mpv_l[key])
                            g_lg[side].SetPoint(g_lg[side].GetN(),x_position,mpv_lg[key]/mpv_mean_lr.get((bar, vov, thr), 1.0))
                            g_lg[side].SetPointError(g_lg[side].GetN()-1,0,mpv_lg_err[key]/mpv_mean_lr.get((bar, vov, thr), 1.0))
                            if i==0:
                                if "L" == side:
                                    g_l[side].SetMarkerColor(2)
                                    g_lg[side].SetMarkerColor(2)
                                    g_lg[side].SetLineColor(2)
                                    f_pol1.SetLineColor(2)
                                elif "R" == side:
                                    g_l[side].SetMarkerColor(4)
                                    g_lg[side].SetMarkerColor(4)
                                    g_lg[side].SetLineColor(4)
                                    f_pol1.SetLineColor(4)
                                elif "L-R" == side:
                                    g_l[side].SetMarkerColor(1)
                                    g_lg[side].SetMarkerColor(1)
                                    g_lg[side].SetLineColor(1)
                                    f_pol1.SetLineColor(1)
                        g_l[side].SetMarkerStyle(24)
                        g_lg[side].SetMarkerStyle(20)
                        res = g_lg[side].Fit(f_pol1, "RS")
                        fit_results[side] = ( f_pol1.GetParameter(1), f_pol1.GetParameter(0) )
                        slope = f_pol1.GetParameter(1)
                        if side == "L":
                            slope *= -1
                            h_slope_mpv.Fill(slope)
                        elif side == "R":
                            h_slope_mpv.Fill(slope)
                        #g_l[side].Draw("P SAME")
                        g_lg[side].Draw("P SAME")
                    latex = ROOT.TLatex()
                    latex.SetNDC(True)
                    latex.SetTextSize(0.045)
                    latex.SetTextFont(42)                    
                    y0 = 0.85                    
                    for i, side in enumerate(sides):
                        if side not in fit_results:
                            continue                        
                        m, q = fit_results[side]                        
                        latex.DrawLatex(0.15, y0 - i*0.06,f"{side}: y = {m:.3f} x + {q:.2f}")
                    c.SaveAs(f"{outdir}/mpv_vs_pos_bar{bar:02d}_Vov{vov:.2f}_th{thr:02d}.png")
                    del g_l
                    del g_lg
                    del hframe

                    # -- draw slope histogram
                    c_slope = ROOT.TCanvas("", "", 600, 500)
                    h_slope_mpv.Draw()
                    N = h_slope_mpv.GetEntries()
                    mu = h_slope_mpv.GetMean()
                    rms = h_slope_mpv.GetRMS()
                    if N > 0:
                        mu_err = rms / math.sqrt(N)
                        rms_err = rms / math.sqrt(2*N)
                    else:
                        mu_err = 0
                        rms_err = 0
                    box = ROOT.TPaveText(0.55, 0.70, 0.88, 0.88, "NDC")
                    box.SetTextAlign(12)
                    box.SetFillColor(0)
                    box.SetTextFont(42)
                    box.SetTextSize(0.05)
                    box.SetBorderSize(0)
                    box.AddText(f"#mu = {mu:.4f} #pm {mu_err:.4f}")
                    box.AddText(f"RMS = {rms:.4f} #pm {rms_err:.4f}")                        
                    box.Draw()
                    c_slope.SaveAs(f"{outdir}/mpv_slope_distribution.png")

                    c = ROOT.TCanvas(f"c_res_vs_pos_bar{bar:02d}_Vov{vov:.2f}_th{thr:02d}","", 600, 500)
                    hframe = ROOT.TH2F("hframe","", 10, xmin, xmax, 10, 0, 0.2)
                    hframe.GetXaxis().SetTitle("x [cm]")
                    hframe.GetYaxis().SetTitle("Energy resolution")
                    hframe.Draw()
                    g_l = {}
                    g_lg = {}
                    g_lg_gaus = {}
                    for j,side in enumerate(sides):
                        g_l[side] = ROOT.TGraph()
                        g_lg[side] = ROOT.TGraph()
                        g_lg_gaus[side] = ROOT.TGraphErrors()
                        for i,label in enumerate(label_list):
                            key=(label,bar,side,vov,thr)
                            if key not in mpv_l:
                                continue
                            x_position = 3.12*label_to_pos[label]/math.cos(math.radians(52))/10
                            g_l[side].SetPoint(g_l[side].GetN(),x_position,res_l[key])
                            g_lg[side].SetPoint(g_lg[side].GetN(),x_position,res_lg[key])
                            g_lg_gaus[side].SetPoint(g_lg_gaus[side].GetN(),x_position,res_lg_gaus[key])
                            g_lg_gaus[side].SetPointError(g_lg_gaus[side].GetN()-1,0,res_lg_gaus_err[key])
                            if "L" == side:
                                g_l[side].SetMarkerColor(2)
                                g_lg[side].SetMarkerColor(2)
                                g_lg_gaus[side].SetMarkerColor(2)
                                g_lg_gaus[side].SetLineColor(2)
                            elif "R" == side:
                                g_l[side].SetMarkerColor(4)
                                g_lg[side].SetMarkerColor(4)
                                g_lg_gaus[side].SetMarkerColor(4)
                                g_lg_gaus[side].SetLineColor(4)
                            elif "L-R" == side:
                                g_l[side].SetMarkerColor(1)
                                g_lg[side].SetMarkerColor(1)
                                g_lg_gaus[side].SetMarkerColor(1)
                                g_lg_gaus[side].SetLineColor(1)
                        g_l[side].SetMarkerStyle(26)
                        g_lg[side].SetMarkerStyle(24)
                        g_lg_gaus[side].SetMarkerStyle(20)
                        # g_l[side].Draw("P SAME")
                        # g_lg[side].Draw("P SAME")
                        g_lg_gaus[side].Draw("PL SAME")
                    c.SaveAs(f"{outdir}/energy_resolution_vs_pos_bar{bar:02d}_Vov{vov:.2f}_th{thr:02d}.png")
                    del g_l
                    del g_lg
                    del g_lg_gaus
                    del hframe


print(" - MPV vs bar plots")
# pars vs bar plots
# ----------------------------
for label in label_list:
    os.makedirs(f"{outdir}/{label}", exist_ok=True)
    for vov in Vovs:
        for thr in thresholds:
            c1 = ROOT.TCanvas("c_mpv_vs_bar_Vov{vov:.2f}_th{thr:02d}","",600,500)
            frame = ROOT.TH2F("frame","",len(bars),0,len(bars)+1,100,150,400)
            frame.GetXaxis().SetTitle("Bar")
            frame.GetYaxis().SetTitle("MPV")
            frame.Draw()
            leg = ROOT.TLegend(0.55,0.70,0.88,0.88)
            leg.SetBorderSize(0)
            leg.SetFillStyle(0)
            g_landau = {}
            g_langaus = {}
            for side in sides:
                g_landau[side] = ROOT.TGraph()
                g_langaus[side] = ROOT.TGraph()
                for i,bar in enumerate(bars):
                    key = (label,bar,side,vov,thr)
                    if key not in mpv_l:
                        continue
                    mpvL = mpv_l[key]
                    mpvLG = mpv_lg[key]
                    g_landau[side].SetPoint(g_landau[side].GetN(),bar,mpvL)
                    g_langaus[side].SetPoint(g_langaus[side].GetN(),bar,mpvLG)
                g_landau[side].SetMarkerStyle(20)
                if "L" == side:
                    g_landau[side].SetMarkerColor(2)
                    g_landau[side].SetLineColor(2)
                elif "R" == side:
                    g_landau[side].SetMarkerColor(4)
                    g_landau[side].SetLineColor(4)
                elif "L-R" == side:
                    g_landau[side].SetMarkerColor(1)
                    g_landau[side].SetLineColor(1)
                # g_landau.SetMarkerStyle(20)
                # g_landau.SetMarkerColor(ROOT.kBlue)
                # g_landau.SetLineColor(ROOT.kBlue)
                # g_langaus.SetMarkerStyle(21)
                # g_langaus.SetMarkerColor(ROOT.kRed)
                # g_langaus.SetLineColor(ROOT.kRed)
                g_landau[side].Draw("PL SAME")
                # g_langaus.Draw("PL SAME")
                leg.AddEntry(g_landau[side],f"{side} - RMS {g_landau[side].GetRMS(2)/g_landau[side].GetMean(2)*100:.0f}%","pl")
                #leg.AddEntry(g_langaus,"MPV Langaus","pl")
                #leg.AddEntry(g_landau,"MPV Landau","pl")
                #leg.AddEntry(g_langaus,"MPV Langaus","pl")
                leg.Draw()
            c1.SaveAs(f"{outdir}/{label}/mpv_vs_bar_Vov{vov:.2f}_th{thr:02d}.png")
            del c1
            del frame
for label in label_list:
    os.makedirs(f"{outdir}/{label}", exist_ok=True)
    for vov in Vovs:
        for thr in thresholds:
            for side in sides:
                # energy resolution vs bar
                c2 = ROOT.TCanvas(f"c_res_vs_bar_{side}_Vov{vov:.2f}_th{thr:02d}","",600,500)
                frame2 = ROOT.TH2F("frame2","",len(bars),0,len(bars)+1,100,0,0.2)
                frame2.GetXaxis().SetTitle("Bar")
                frame2.GetYaxis().SetTitle("Energy resolution")
                frame2.Draw()
                leg2 = ROOT.TLegend(0.45,0.65,0.88,0.88)
                leg2.SetBorderSize(0)
                leg2.SetFillStyle(0)
                g_res_l = ROOT.TGraph()
                g_res_gaus = ROOT.TGraph()
                g_res_fwhm = ROOT.TGraph()
                for i,bar in enumerate(bars):
                    key = (label, bar,side,vov,thr)
                    if key not in res_l:
                        continue
                    resl = res_l[key]
                    resg = res_lg_gaus[key]
                    resf = res_lg[key]
                    g_res_l.SetPoint(g_res_l.GetN(),bar,resl)
                    g_res_gaus.SetPoint(g_res_gaus.GetN(),bar,resg)
                    g_res_fwhm.SetPoint(g_res_fwhm.GetN(),bar,resf)
                g_res_l.SetMarkerStyle(20)
                g_res_l.SetMarkerColor(ROOT.kViolet-2)
                g_res_l.SetLineColor(ROOT.kViolet-2)
                g_res_gaus.SetMarkerStyle(21)
                g_res_gaus.SetMarkerColor(ROOT.kTeal-5)
                g_res_gaus.SetLineColor(ROOT.kTeal-5)
                g_res_fwhm.SetMarkerStyle(22)
                g_res_fwhm.SetMarkerColor(ROOT.kOrange-3)
                g_res_fwhm.SetLineColor(ROOT.kOrange-3)
                g_res_l.Draw("PL SAME")
                g_res_gaus.Draw("PL SAME")
                #g_res_fwhm.Draw("PL SAME")
                leg2.AddEntry(g_res_l,"Landau (Width/MPV)","pl")
                leg2.AddEntry(g_res_gaus,"Langaus (#sigma_{G}/MPV)","pl")
                #leg2.AddEntry(g_res_fwhm,"Langaus (Width/MPV)","pl")
                leg2.Draw()
                c2.SaveAs(f"{outdir}/{label}/energy_resolution_vs_bar_{side}_Vov{vov:.2f}_th{thr:02d}.png")
                del frame2
                del c2
remove_useless_dirs(outdir)
