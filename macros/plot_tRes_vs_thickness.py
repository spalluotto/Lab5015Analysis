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
    
# define graphs
graphs = {
    "data"  : ROOT.TGraph(),
    "Stoch" : ROOT.TGraph(),
    "Noise" : ROOT.TGraph(),
    "SR"    : ROOT.TGraph()
}

graphs_scaled = graphs.copy()

plot_settings = {
    "data"  : ["time resolution [ps]", 1],
    "Stoch" : ["#sigma_{stoch} [ps]", ROOT.kGreen+2],
    "Noise" : ["#sigma_{noise} [ps]", ROOT.kBlue],
    "SR"    : ["slew rate at the timing threshold", 1]
}
fit = {
    "data"  : "[0]/sqrt(x)",
    "Stoch" : "[0]/sqrt(x)",
    "Noise" : "[0]/x",
    "SR"    : "[0]*x"
    }

if irr:
    graphs["DCR"] = ROOT.TGraph()
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

# Loop over the dictionary to retrieve and evaluate the graphs
for module, thickness in modules.items():
    for g in graphs:
        graph = file.Get(f"g_{g}_vs_Vov_average_{module}")
        if not graph:
            raise ValueError(f"Error retrieving graph {g} for {module} from the file")
    
        y_value = graph.Eval(ov_ref)
        graphs[g].SetPoint(graphs[g].GetN(), thickness, y_value)

        if '/sqrt' in fit[g]:
            y_scaled = y_value/math.sqrt(enScale[g])
        elif '/x' in fit[g]:
            y_scaled = y_value/enScale[g]
        elif '*x' in fit[g]:
            y_scaled = y_value*enScale[g]

# draw
for g in graphs:
    y_label = plot_settings[g][0]
    col = plot_settings[g][1]
    c = ROOT.TCanvas(f"c_{g}_vs_thickness", f"c_{g}_vs_thickness", 600, 500)
    c.cd()
    hPad = ROOT.gPad.DrawFrame(2,0,4,70)
    hPad.SetTitle(f";thickness [mm];{y_label}")
    hPad.Draw()

    graphs[g].SetMarkerColor(col)
    graphs[g].SetMarkerStyle(20)
    graphs[g].Draw("PSAME")


    if irr:
        f = ROOT.TF1("func", fit[g], 2,4)
        f.SetLineColor(col)
        graphs[g].Fit(f, "RS+")
        
        chi = f.GetChisquare()
        ndf = f.GetNDF()
        p_value = ROOT.TMath.Prob(chi, ndf)

        print("\n\n p-value : ", p_value)
    
    
    c.SaveAs(f"{plotdir}/{c.GetName()}_{label}.png")
