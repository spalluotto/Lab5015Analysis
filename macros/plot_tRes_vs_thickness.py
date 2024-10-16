import os, ROOT
import CMS_lumi, tdrstyle
from utils import *
from SiPM import *

#set the tdr style                                                                                                                                                                                     
tdrstyle.setTDRStyle()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetLabelSize(0.055,'X')
ROOT.gStyle.SetLabelSize(0.055,'Y')
ROOT.gStyle.SetTitleSize(0.07,'X')
ROOT.gStyle.SetTitleSize(0.07,'Y')
ROOT.gStyle.SetTitleOffset(1.05,'X')
ROOT.gStyle.SetTitleOffset(1.1,'Y')
ROOT.gStyle.SetLegendFont(42)
ROOT.gStyle.SetLegendTextSize(0.045)
ROOT.gStyle.SetPadTopMargin(0.07)
ROOT.gStyle.SetPadRightMargin(0.05)
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning

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

stochPow = 0.73

plotdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23//plot_tRes_vs_thickness/'
indir = '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/'

latexOnTop = True
label_on_top = 'HPK'

if irr:
    # ----- irradiated modules
    infile = f'{indir}/plot_tRes_HPK_2E14_T-35C_angle64_types'
    label = 'types_2E14'
    irr_label = '2 #times 10^{14} 1 MeV n_{eq}/cm^{2}'
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
    irr_label = 'non-irradiated'

    if refTh:
        infile+='_refTh'
        label+='_refTh'

    infile+='.root'

    modules = {
        "HPK_nonIrr_LYSO818_angle64_T5C": 3.75,
        "HPK_nonIrr_LYSO813_angle64_T5C": 3.0,
        "HPK_nonIrr_LYSO816_angle64_T5C": 2.4
    }


if refTh:
    label += "_refTh"
    
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
    fit["DCR"] = "[0]/x"




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


ov_ref = 0.95
file = ROOT.TFile(infile)

# Loop over the dictionary to retrieve and evaluate the graphs + compute the scaling
for module, thickness in modules.items():
    for g in graphs:
        if g=="data" or g=="Noise" or g=="SR": # require a different procedure
            continue
        if g=="Stoch" and not irr:
            graph = file.Get(f"g_{g}Meas_vs_Vov_average_{module}")
        else:
                graph = file.Get(f"g_{g}_vs_Vov_average_{module}")
        if not graph:
            raise ValueError(f"Error retrieving graph {g} for {module} from the file")
    
        y_value = graph.Eval(ov_ref)
        y_error = interp1d(graph.GetX(), graph.GetEY(), kind='linear')(ov_ref) # interpolating error associated to evaluated point
        
        if '/sqrt' in fit[g]:
            y_scaled = y_value/math.pow(enScale[g],stochPow)
            y_error = y_error/math.pow(enScale[g],stochPow)
        elif '/x' in fit[g]:
            y_scaled = y_value/enScale[g]
            y_error = y_error/enScale[g]
        
        graphs[g].SetPoint(graphs[g].GetN(), thickness, y_scaled)
        graphs[g].SetPointError(graphs[g].GetN()-1, 0, y_error)
        
# scaling applied first on SR , then noise re-computed
for module, thickness in modules.items():
    g="Noise"
    g_sr = file.Get(f"g_SR_vs_Vov_average_{module}")
    sr = g_sr.Eval(ov_ref)                              
    err_sr = interp1d(g_sr.GetX(), g_sr.GetEY(),kind='linear')(ov_ref)
    noise,err_noise = sigma_noise(sr*enScale[g], '2c',err_sr*enScale[g])
    graphs[g].SetPoint(graphs[g].GetN(), thickness, noise)
    graphs[g].SetPointError(graphs[g].GetN()-1, 0, err_noise)
    
    
print("V_ov ", ov_ref)
# data computed as sum in quadrature
i = 0
for module, thickness in modules.items():
    g = "data"
    par = "Stoch"
    s_stoch = graphs[par].GetY()[i]
    err_s_stoch = graphs[par].GetEY()[i]
    
    par = "Noise"
    s_noise = graphs[par].GetY()[i]
    err_s_noise = graphs[par].GetEY()[i]

    par = "DCR"
    s_dcr = 0
    err_s_dcr = 0

    if irr:
        s_dcr = graphs[par].GetY()[i]
        err_s_dcr = graphs[par].GetEY()[i]

    s_tot = math.sqrt(s_noise*s_noise + s_stoch*s_stoch + s_dcr*s_dcr)
    err_s_tot = 1./s_tot * math.sqrt( pow( err_s_stoch*s_stoch,2) + pow(s_noise*err_s_noise,2) + pow(s_dcr*err_s_dcr,2))
    
    graphs[g].SetPoint(graphs[g].GetN(), thickness, s_tot)
    graphs[g].SetPointError(graphs[g].GetN()-1, 0, err_s_tot)

    i +=1
    
    print("thickness: ", thickness, "\t data scaled : ", round(s_tot,2))
    
# draw
c = ROOT.TCanvas("c_timeResolution_vs_thickness", "c_timeResolution_vs_thickness", 600, 500)
c.cd()

hPad = ROOT.gPad.DrawFrame(2.2,0,4,100)
hPad.SetTitle(f";;time resolution [ps]")
ROOT.gPad.SetTicks(1)

#hPad.Draw()
# Create a TGaxis object with no labels
x_axis = ROOT.TGaxis(2.2, 0, 4, 0, 2.2, 4, 510, "+L")
x_axis.SetLabelSize(0)  # Hide default x-axis labels
x_axis.SetTitle("crystal thickness [mm]")
x_axis.SetTitleFont(42)
x_axis.SetTitleSize(0.07)
x_axis.SetTitleOffset(1.05)
x_axis.SetLabelColor(0)
x_axis.SetLabelSize(0)
x_axis.SetLabelOffset(999)
x_axis.SetTickLength(0.03)
x_axis.SetNdivisions(3)  # This will keep the ticks but hide labels
x_axis.Draw("same")

# Define positions and labels
x_positions = [2.4, 3.0, 3.75]  # X positions where you want labels
x_labels = ["T3", "T2", "T1"]

# Draw custom x-axis labels using TLatex
latex_t = {}
for x, lab in zip(x_positions, x_labels):
    latex_t[lab] = ROOT.TLatex(x, 5, lab)  # Adjust y-coordinate (-10) to place the label below the axis
    latex_t[lab].SetTextSize(0.05)
    latex_t[lab].SetTextAlign(22)  # Center align the text
    latex_t[lab].Draw()



for g in graphs:
    if g=="SR":
        continue
    col = plot_settings[g][1]
    graphs[g].SetLineWidth(2)
    graphs[g].SetLineColor(col)
    graphs[g].SetMarkerColor(col)
    
    if g!="data":
        graphs[g].SetFillColor(col)
        graphs[g].SetFillColorAlpha(col, 0.5)
        if g=='Stoch':
            graphs[g].SetFillStyle(3001)
        elif g=='Noise':
            graphs[g].SetFillStyle(3004)
        elif g=='DCR':
            graphs[g].SetFillStyle(3005)
    else:
        graphs[g].SetMarkerStyle(20)
        graphs[g].SetLineColor(col)

    #"""
    if (g=="data"):
        f = ROOT.TF1("func", "[0]*pow(x,[1])", 2.3,3.85)
        f.SetLineColor(col)
        f.SetLineStyle(7)
        f.SetLineWidth(2)
        f.SetNpx(50)
        graphs[g].Fit(f, "RS+")
        chi = f.GetChisquare()
        ndf = f.GetNDF()
        p_value = ROOT.TMath.Prob(chi, ndf)
        print("\n\n p-value : ", p_value)
        graphs[g].Draw("PSAME")

        tl3 = ROOT.TLatex()
        tl3.SetNDC()
        tl3.SetTextFont(42)
        tl3.SetTextSize(0.050)
        tl3.DrawLatex(0.20,0.80,'(%.0f #pm %.0f) x thickness^{%.2f #pm %.2f}'%(f.GetParameter(0), f.GetParError(0),f.GetParameter(1), f.GetParError(1) ))
    else:
        graphs[g].Draw("E3SAMEPL")
    #"""

    """
    if (g=="data"):
        graphs[g].Draw("PLSAME")
    else:
        graphs[g].Draw("E3SAMEPL")
    """
    leg = ROOT.TLegend(0.7, 0.60, 0.89, 0.89)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.050)
    leg.AddEntry(graphs["data"], 'data', 'PL')
    leg.AddEntry(graphs["Noise"], 'electronics', 'FL')
    leg.AddEntry(graphs["Stoch"], 'photo-stat.', 'FL')

    if irr:
        leg.AddEntry(graphs["DCR"], 'DCR', 'FL')
    leg.Draw()


    
#cms_logo = draw_logo()
#cms_logo.Draw()    

tl2 = ROOT.TLatex()
tl2.SetNDC()
tl2.SetTextFont(42)
tl2.SetTextSize(0.045)
if latexOnTop:
    tl2.DrawLatex(0.20,0.86,'%s'%label_on_top)  # scritta in alto                                                                                                                                                                                                                        
else:
    tl2.DrawLatex(0.20,0.26,'%s'%label_on_top) # scritta in basso                                                                                                                                                                                                                        


tl = ROOT.TLatex()
tl.SetNDC()
tl.SetTextFont(42)
tl.SetTextSize(0.045)
if latexOnTop:
    tl.DrawLatex(0.20,0.80, irr_label) # scritta in alto                                                                                                                                                                                                                                 
else:
    tl.DrawLatex(0.20,0.20, irr_label) # scritta in basso     


x_axis.Draw("same")
c.Update()
c.SaveAs(f"{plotdir}/{c.GetName()}_{label}.png")
print(f"saved as {plotdir}/{c.GetName()}_{label}.png")
