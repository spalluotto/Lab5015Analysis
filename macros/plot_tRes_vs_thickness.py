import os, ROOT
import CMS_lumi, tdrstyle
from utils import *
from SiPM import *


# ----- EDIT -----
irr    = False
refTh  = False
# ----------------

plotdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'
indir = '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/'



if irr:
    # ----- irradiated modules
    infile = f'{indir}/plot_tRes_HPK_2E14_T-35C_angle64_types'
    label = 'types_2E14'

    if refTh:
        infile+='_refTh.root'
        label+='_refTh'
    else:
        infile+='.root'

    graphs_info = {
        "HPK_2E14_LYSO100056_angle64_T-35C": 3.75,
        "HPK_2E14_LYSO815_angle64_T-35C": 3.0,
        "HPK_2E14_LYSO300032_angle64_T-35C": 2.4
    }
else:
    # ---- non irradiated 
    infile = f'{indir}/plot_tRes_HPK_nonIrr_angle64_T5C_types'
    label = 'types_nonIrr'

    if refTh:
        infile+='_refTh.root'
        label+='_refTh'
    else:
        infile+='.root'

    graphs_info = {
        "HPK_nonIrr_LYSO818_angle64_T5C": 3.75,
        "HPK_nonIrr_LYSO813_angle64_T5C": 3.0,
        "HPK_nonIrr_LYSO816_angle64_T5C": 2.4
    }
    
# define x and y values
thicknesses = []
evaluations = []

ov_ref = 1.0

file = ROOT.TFile(infile)

# Loop over the dictionary to retrieve and evaluate the graphs
for graph_name, thickness in graphs_info.items():
    graph = file.Get(f"g_data_vs_Vov_average_{graph_name}")
    if not graph:
        raise ValueError(f"Error retrieving graph {graph_name} from the file")
    
    y_value = graph.Eval(ov_ref)
    
    thicknesses.append(thickness)
    evaluations.append(y_value)

# create graph
thickness_graph = ROOT.TGraph(len(thicknesses))
for i, (thickness, evaluation) in enumerate(zip(thicknesses, evaluations)):
    thickness_graph.SetPoint(i, thickness, evaluation)

# draw
c = ROOT.TCanvas("c_timeResolution_vs_thickness", "c_timeResolution_vs_thickness", 600, 500)
c.cd()
hPad = ROOT.gPad.DrawFrame(2,0,4,70)
hPad.SetTitle(";thickness [mm];time resolution [ps]")
hPad.Draw()

thickness_graph.SetMarkerStyle(20)
thickness_graph.Draw("PLSAME")

c.SaveAs(f"{plotdir}/timeResolution_vs_thickness_{label}.png")
