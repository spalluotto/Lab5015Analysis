import os, ROOT
import CMS_lumi, tdrstyle
from utils import *
from SiPM import *

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--irrad", action='store_true',  help="consider irr types")
parser.add_argument("-r",  '--refTh', action='store_true',  help="use a fixed threshold instead of the best threshold")
args = parser.parse_args()


# ----- EDIT -----
irr    = args.irrad
refTh  = args.refTh
angle_true = 49
angle_offset = 3
# ----------------

plotdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23//plot_tRes_vs_thickness/'
indir = '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/'

print("------------------------\n----------------------------\n\n IN TUTTO CIO MANCANO GLI ERRORI \n\n------------------------\n----------------------------\n\n")


if irr:
    # ----- irradiated modules
    infile = f'{indir}/plot_tRes_HPK_2E14_T-35C_angle64_types'
    label = 'types_2E14'
    if refTh:
        infile+='_refTh'
        label+='_refTh'

    infile+='.root'

    modules = {
        "HPK_2E14_LYSO100056_angle64_T-35C": 3.75,
        "HPK_2E14_LYSO815_angle64_T-35C": 3.0,
        "HPK_2E14_LYSO300032_angle64_T-35C": 2.4
    }
else:
    # ---- non irradiated 
    infile = f'{indir}/plot_tRes_HPK_nonIrr_angle64_T5C_types'
    label = 'types_nonIrr'

    if refTh:
        infile+='_refTh'
        label+='_refTh'

    infile+='.root'

    modules = {
        "HPK_nonIrr_LYSO818_angle64_T5C": 3.75,
        "HPK_nonIrr_LYSO813_angle64_T5C": 3.0,
        "HPK_nonIrr_LYSO816_angle64_T5C": 2.4
    }
    
# define graphs scaled
graphs = {
    "data"  : ROOT.TGraphErrors(),
    "Stoch" : ROOT.TGraphErrors(),
    "Noise" : ROOT.TGraphErrors(),
    "SR"    : ROOT.TGraphErrors()
}


plot_settings = {
    "data"  : ["time resolution [ps]", 1],
    "Stoch" : ["#sigma_{stoch} [ps]", ROOT.kGreen+2],
    "Noise" : ["#sigma_{noise} [ps]", ROOT.kBlue],
    "SR"    : ["slew rate at the timing threshold", 1]
}
fit = {
    "data"  : "[0]/pow(x,[1])",
    "Stoch" : "[0]/sqrt(x)",
    "Noise" : "[0]/x",
    "SR"    : "[0]*x"
    }

if irr:
    graphs["DCR"] = ROOT.TGraphErrors()
    plot_settings["DCR"] = ["#sigma_{DCR} [ps]", ROOT.kOrange+2]
    fit["DCR"] = "[0]/sqrt(x)"




# --- energy scaling ----
enScale = {}
for it,g in enumerate(graphs):
    if not isinstance(angle_true, list):
        ang_true = angle_true
        angle_target = angle_true + angle_offset
    else:
        ang_true = angle_true[it]
        angle_target = angle_true[it] + angle_offset
    enScale[g] = math.cos(math.radians(ang_true)) / math.cos(math.radians(angle_target))


ov_ref = 1.0
file = ROOT.TFile(infile)

# Loop over the dictionary to retrieve and evaluate the graphs + compute the scaling
for module, thickness in modules.items():
    for g in graphs:
        if g=="data" or g=="Noise": # require a different procedure
            continue
        if g=="Stoch" and not irr:
            graph = file.Get(f"g_{g}Meas_vs_Vov_average_{module}")
        else:
                graph = file.Get(f"g_{g}_vs_Vov_average_{module}")
        if not graph:
            raise ValueError(f"Error retrieving graph {g} for {module} from the file")
    
        y_value = graph.Eval(ov_ref)

        if '/sqrt' in fit[g]:
            y_scaled = y_value/math.sqrt(enScale[g])
        elif '*x' in fit[g]:
            y_scaled = y_value*enScale[g]
        
        graphs[g].SetPoint(graphs[g].GetN(), thickness, y_scaled)

# scaling applied first on SR , then noise re-computed
for module, thickness in modules.items():
    g="Noise"
    g_sr = file.Get(f"g_SR_vs_Vov_average_{module}")
    sr = g_sr.Eval(ov_ref)                               # FIX ME : interpolation for errors!!!!!
    noise,err_noise = sigma_noise(sr*enScale[g], '2c',sr*enScale[g]/10)
    graphs[g].SetPoint(graphs[g].GetN(), thickness, noise)


# data computed as sum in quadrature
for module, thickness in modules.items():
    g = "data"
    s_stoch = graphs["Stoch"].Eval(thickness)
    s_noise = graphs["Noise"].Eval(thickness)
    s_dcr = 0
    if irr:
        s_dcr = graphs["DCR"].Eval(thickness)
    s_tot = math.sqrt(s_noise*s_noise + s_stoch*s_stoch + s_dcr*s_dcr)
    graphs[g].SetPoint(graphs[g].GetN(), thickness, s_tot)
    
# draw
c = ROOT.TCanvas("c_timeResolution_vs_thickness", "c_timeResolution_vs_thickness", 600, 500)
c.cd()
hPad = ROOT.gPad.DrawFrame(2,0,4,70)
hPad.SetTitle(f";thickness [mm];time resolution [ps]")
hPad.Draw()
for g in graphs:
    if g=="SR":
        continue
    col = plot_settings[g][1]
    graphs[g].SetMarkerColor(col)
    graphs[g].SetLineColor(col)
    graphs[g].SetMarkerStyle(20)
    

    if (irr and g=="data") or (not irr and g=="Stoch"):
        graphs[g].Draw("PSAME")
        f = ROOT.TF1("func", "[0]/pow(x,[1])", 2,4)
        f.SetLineColor(col)
        graphs[g].Fit(f, "RS+")
        
        chi = f.GetChisquare()
        ndf = f.GetNDF()
        p_value = ROOT.TMath.Prob(chi, ndf)

        print("\n\n p-value : ", p_value)
    else:
        graphs[g].Draw("PLSAME")

    
c.SaveAs(f"{plotdir}/{c.GetName()}_{label}.png")
