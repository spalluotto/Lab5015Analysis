import os, ROOT
import CMS_lumi, tdrstyle
from utils import *
from SiPM import *
from moduleDict import * 
ROOT.gStyle.SetOptFit(1)

plotdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'
indir = '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/'

files = {
    'LYSO829'    : ['12', '0', '-19', '-32'],
    'LYSO819'    : ['-22', '-27', '-32', '-37'],
    'LYSO100056' : ['-30', '-35', '-40'],    
}

g_sDCR_vs_DCRNpe_average = {}

for module in files:
    g_sDCR_vs_DCRNpe_average[module] = {}
    sipm = sipm_(module)
    infile = f'{indir}/plot_tRes_{sipm}_{module}_temperatures.root'
    temperatures = files[module]
    file = ROOT.TFile(infile)
    print(temperatures)
    for t in temperatures:
        print(module, '  ', t)
        conf_label = f'{sipm}_{module}_angle52_T{t}C'
        g_sDCR_vs_DCRNpe_average[module][t] = file.Get(f'g_DCR_vs_DCRNpe_average_{conf_label}')

# --- draw 
c = ROOT.TCanvas("c_sigmaDCR_vs_DCRtoNpe", "c_sigmaDCR_vs_DCRtoNpe", 600, 500)
c.cd()
hPad = ROOT.gPad.DrawFrame(0,0,0.5,70)
hPad.SetTitle(";#sqrt{DCR/30GHz}/(Npe/3000);#sigma_{t}^{DCR} [ps]")
hPad.Draw()

leg = ROOT.TLegend(0.2,0.55,0.6,0.9)
mg = ROOT.TMultiGraph()
it=0
for module in files:
    temperatures = files[module]
    for t in temperatures:
        g_sDCR_vs_DCRNpe_average[module][t].SetMarkerStyle(20+it*2)
        g_sDCR_vs_DCRNpe_average[module][t].Draw("PSAME")
        mg.Add(g_sDCR_vs_DCRNpe_average[module][t])
        leg.AddEntry(g_sDCR_vs_DCRNpe_average[module][t], f"{sipm_(module).split('HPK_')[1]} T {t}C", "p")
    it+=1

f = ROOT.TF1("func", "[0] * pow(x,[1])", 0,0.5)
f.SetNpx(1000)
f.SetLineWidth(2)
f.SetLineStyle(2)
f.SetLineColor(1)
f.SetParameter(0,30)
f.SetParameter(1,0.5)
mg.Fit(f, "RS")
f.Draw("SAME")
    
leg.Draw("same")    
c.SaveAs(f'{plotdir}/{c.GetName()}.png')

        
