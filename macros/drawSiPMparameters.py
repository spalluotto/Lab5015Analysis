import os, ROOT
from ctypes import c_double, c_float
import CMS_lumi, tdrstyle
from utils import *

pde_scale = {
    "HPK" : 1.016,
    "FBK" : 0.863
}


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


colors = [ROOT.kRed,ROOT.kBlue,ROOT.kGreen+2,ROOT.kOrange+1]
markers_hpk = [22,21,20,23]
markers_fbk = [26,25,24,32]

def graphs_from_files(files_list, parameter, plot_name, yset, canvas_name="canvas"):
    canv_name = canvas_name
    canv = ROOT.TCanvas(canvas_name, canvas_name, 600,500)
    canv.cd()
    hPad = ROOT.gPad.DrawFrame(0,0,5,yset[0])
    hPad.SetTitle(f";OV [V];{yset[1]}")
    hPad.Draw()
    #canv = CMS.cmsCanvas(canv_name,0,5,0,yset[0],"OV [V]",yset[1],square=CMS.kSquare,extraSpace=0.01,iPos=0)

    leg = ROOT.TLegend(0.20, 0.70, 0.37, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.050)

    leg_prod = ROOT.TLegend(0.39, 0.70, 0.65, 0.9)
    leg_prod.SetBorderSize(0)
    leg_prod.SetFillColor(0)
    leg_prod.SetTextFont(42)
    leg_prod.SetTextSize(0.050)

    root_file = ROOT.TFile.Open(files_list[0])
    keys = root_file.GetListOfKeys()

    j= 0
    for f in files_list:
        rf = ROOT.TFile.Open(f)
        it = 0
        for key in keys:
            if parameter in key.GetName():
                graph_name = key.GetName()
                graph = rf.Get(graph_name)
                if graph:
                    vendor = f.split("/")[-1].split("_")[0]
                    if parameter == "pde":
                        # Apply the scaling to the y-values for PDE
                        for i in range(graph.GetN()):
                            x, y = c_double(0.0), c_double(0.0)
                            graph.GetPoint(i, x, y)
                            graph.SetPoint(i, x, y.value * pde_scale[vendor])

                    # legend for vendors
                    if it == 0:
                        leg_prod.AddEntry(graph, vendor,"p")

                    # legend for cell size
                    if 'HPK' in f:
                        graph.SetMarkerStyle(markers_hpk[it])
                        leg.AddEntry(graph, graph_name.split("_")[1].replace("u", "#mu"),"p")
                        print(graph_name)
                    else:
                        graph.SetMarkerStyle(markers_fbk[it])

                    graph.SetLineColor(colors[it])
                    graph.SetMarkerColor(colors[it])
                    graph.Draw("PSAME" if canv.GetListOfPrimitives().GetSize() else "P")                        
                    it += 1       
                else:
                    print("in ", f, "  ", graph_name, " not found")
        j+=1

    hPad.GetYaxis().SetMaxDigits(3)
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    leg.Draw("same")
    leg_prod.Draw("same")
    #cms_logo = draw_logo()
    #cms_logo.Draw()
    
    canv.SaveAs(plot_name)



    
if __name__ == "__main__":
    rootdir = '/eos/home-s/spalluot/MTD/CERN/SiPM_parameters'
    infiles = ['{}/FBK_parameters.root'.format(rootdir), "{}/HPK_parameters.root".format(rootdir)]
    plotdir = '/eos/home-s/spalluot/www/MTD/CERN/SiPM_parameters'
    parameters = ['pde', 'gain']
    yaxis = {
        "pde" : [0.8, "Effective PDE"],
        "gain" : [2e6, "Gain"]
    }

    
    for par in parameters:
        plotname = '{}/{}.png'.format(plotdir, par)
        graphs_from_files(infiles, par, plotname, yaxis[par], canvas_name=par)
