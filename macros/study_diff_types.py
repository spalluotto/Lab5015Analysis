#! /usr/bin/env python
import os
import shutil
import glob
import math
import array
import sys
import time
import argparse

import ROOT
import tdrstyle
from SiPM import *
from slewRate import *
from moduleDict import *

ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.SetBatch(False)
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0111)


#--------CAMBIA QUI------------------------------------------------------------------

comparisonNum = 1

if comparisonNum == 1:
    sipmTypes = ['HPK_nonIrr_C25_LYSO818','HPK_nonIrr_C25_LYSO813','HPK_nonIrr_C25_LYSO816']
    outSuffix = 'HPK_nonIrr_C25'
    extraLabel = ['','','']
    extraName = ['','','']
    modType = [1,2,3]

#--------------------------------------------------------------------------------------

# ----- output --------
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_FNAL_Mar23/study_diff_types/%s/'%outSuffix
if (os.path.exists(outdir)==False):
    os.mkdir(outdir)


for it,sipm in enumerate(sipmTypes):
    sipmTypes[it] = sipm + '_T12C' + extraName[it]

#---------



fnames = {}
labels = {}
cols = {}
markers = {}
LO = {}
tau = {}
tauRise = {}
NpeFrac = {}

for it, sipm in enumerate(sipmTypes):
    fnames[sipm] = '../plots/plot_tRes_%s.root'%(sipm)
    labels[sipm] = label_(sipm) + extraLabel[it]
    cols[sipm] = color_(sipm)
    markers[sipm] = 20
    LO[sipm] = light_output(sipm)
    tau[sipm] = tau_decay(sipm)
    tauRise[sipm] = tau_rise(sipm)
    NpeFrac[sipm] = Npe_frac(sipm)

graphs_t = {
    'timeResolutionAve': [1,   'data'],
    'NoiseAve'         : [600, 'noise'],
    'StochAve'         : [418, 'stoch'],
    'TotExpAve'        : [633, 'stoch #oplus noise']
    }

graphs_SR = ['slewRate', 'Npe', 'StochMeasAve']
# --- retrieve bars and ovs from plot t res
VovsUnion = []

g_t = {}
g_SR = {}
Vovs = {}
for j,sipm in enumerate(sipmTypes):
    f = ROOT.TFile.Open(fnames[sipm])
    g_t[sipm] = {}
    g_SR[sipm] = {}
    Vovs[sipm] = []
    for it, graph in enumerate(graphs_t):
        g_t[sipm][graph] = f.Get('g_%s_vs_Vov'%graph)
        if it == 0:
            for ipoint in range(g_t[sipm][graph].GetN()):
                Vovs[sipm].append(g_t[sipm][graph].GetX()[ipoint])
    if j == 0:  
        VovsUnion = Vovs[sipm]
    else:
        VovsUnion = union(VovsUnion, Vovs[sipm]) 
    for graph in graphs_SR:
        g_SR[sipm][graph] = f.Get('g_%s_vs_Vov'%graph)
        

#----- time resolution: splitting contributions --
g_t_vs_type = {}

for ov in VovsUnion:
    g_t_vs_type[ov] = {}
    for graph in graphs_t:
        g_t_vs_type[ov][graph] = ROOT.TGraphErrors()
        for it, sipm in enumerate(sipmTypes):
            if ov not in Vovs[sipm]: continue
            g_t_vs_type[ov][graph].SetPoint(g_t_vs_type[ov][graph].GetN(), modType[it], g_t[sipm][graph].Eval(ov))
            erY = 0
            for ipoint in range(g_t[sipm][graph].GetN()):
                print 'g_t[sipm][graph].Eval(ov) ', g_t[sipm][graph].Eval(ov), '    g_t[sipm][graph].GetX()[ipoint]    ', g_t[sipm][graph].GetX()[ipoint]
                if ov == g_t[sipm][graph].GetX()[ipoint]:
                    erY = g_t[sipm][graph].GetErrorY(ipoint)                
                    print 'erY: ', erY
            g_t_vs_type[ov][graph].SetPointError(g_t_vs_type[ov][graph].GetN()-1, 0, erY)

            # print 'ov: ', ov , '\tgraph: ', graph, '\tsipm: ', sipm, '\tsigma= ', g_t[sipm][graph].Eval(ov)


g_Stoch_vs_Npe = {}
g_Npe_vs_PDE   = {}
g_SR_vs_model  = {}

for ov in VovsUnion:
    g_Stoch_vs_Npe[ov] = {}
    g_Npe_vs_PDE[ov]   = {}
    g_SR_vs_model[ov]  = {}
    for sipm in sipmTypes:
        if ov not in Vovs[sipm]: continue
        g_Stoch_vs_Npe[ov][sipm] = ROOT.TGraphErrors() 
        g_Npe_vs_PDE[ov][sipm]   = ROOT.TGraphErrors()
        g_SR_vs_model[ov][sipm]  = ROOT.TGraphErrors()

        g_Stoch_vs_Npe[ov][sipm].SetPoint(g_Stoch_vs_Npe[ov][sipm].GetN(), g_SR[sipm]['Npe'].Eval(ov), g_SR[sipm]['StochMeasAve'].Eval(ov))
        g_Npe_vs_PDE[ov][sipm].SetPoint(g_Npe_vs_PDE[ov][sipm].GetN(), PDE(ov,sipm), g_SR[sipm]['Npe'].Eval(ov))
        g_SR_vs_model[ov][sipm].SetPoint(g_SR_vs_model[ov][sipm].GetN(), SR_model(sipm), g_SR[sipm]['slewRate'].Eval(ov))



# ---- draw splitting ----
for ov in VovsUnion:
    c = ROOT.TCanvas('c_timeResolution_vs_type_Vov%.2f'%ov, '', 900, 700)
    c.cd()
    c.SetGridy()
    
    hPad = ROOT.TH2F('','',100,0.5,4,100,0,120)
    hPad.GetXaxis().SetTitle('module type')
    hPad.GetYaxis().SetTitle('#sigma_{t} [ps]')
    hPad.Draw()
    
    leg = ROOT.TLegend(0.70,0.70,0.89,0.89)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    for j,graph in enumerate(g_t_vs_type[ov]):
        if 'timeResolution' in graph:
            g_t_vs_type[ov][graph].SetMarkerStyle(20)
            g_t_vs_type[ov][graph].SetMarkerSize(1)
            g_t_vs_type[ov][graph].SetLineColor(0)
            g_t_vs_type[ov][graph].SetMarkerColor(graphs_t[graph][0])
            g_t_vs_type[ov][graph].Draw('psame')
        else:
            g_t_vs_type[ov][graph].SetLineColor(graphs_t[graph][0])
            g_t_vs_type[ov][graph].SetFillColor(graphs_t[graph][0])
            g_t_vs_type[ov][graph].SetFillColorAlpha(graphs_t[graph][0], 0.5)
            g_t_vs_type[ov][graph].SetFillStyle(3001)
            g_t_vs_type[ov][graph].SetLineWidth(2)
            g_t_vs_type[ov][graph].Draw('E3lsame')

        leg.AddEntry(g_t_vs_type[ov][graph], '%s'%graphs_t[graph][1], 'pl')
    leg.Draw('same')
    latex = ROOT.TLatex(0.15,0.83,'Vov%.2f'%ov)
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextFont(42)
    latex.Draw('same')
            
    c.SaveAs(outdir+'/'+c.GetName()+'.png')




#---- draw plots : stoch vs Npe  ------
#---- 
mg = {}
f_Stoch_vs_Npe = {}
for ov in VovsUnion:
    c = ROOT.TCanvas('c_Stoch_vs_Npe_Vov%.2f'%ov, '', 900, 700)
    c.cd()
    c.SetGridy()
    
    hPad = ROOT.TH2F('','',100,1000,10000,100,0,120)
    hPad.GetXaxis().SetTitle('N_{phe}')
    hPad.GetYaxis().SetTitle('#sigma_{t}^{stoch} [ps]')
    hPad.Draw()
    
    leg = ROOT.TLegend(0.70,0.70,0.89,0.89)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)

    f_Stoch_vs_Npe[ov] = ROOT.TF1('f_Stoch_vs_Npe_Vov%.2f'%ov, '[0]*x^{[1]}', 1000, 10000)
    f_Stoch_vs_Npe[ov].SetLineColor(ROOT.kGreen+2)
    
    mg[ov] = ROOT.TMultiGraph()

    for sipm in sipmTypes:
        if ov not in Vovs[sipm]: continue
        g_Stoch_vs_Npe[ov][sipm].SetMarkerStyle(20)
        g_Stoch_vs_Npe[ov][sipm].SetMarkerSize(1)
        g_Stoch_vs_Npe[ov][sipm].SetLineColor(color_(sipm))
        g_Stoch_vs_Npe[ov][sipm].SetMarkerColor(color_(sipm))
        g_Stoch_vs_Npe[ov][sipm].Draw('psame')
        mg[ov].Add(g_Stoch_vs_Npe[ov][sipm])
        leg.AddEntry(g_Stoch_vs_Npe[ov][sipm], '%s'%label_(sipm), 'pl')

    mg[ov].Fit(f_Stoch_vs_Npe[ov])
    leg.Draw('same')
    f_Stoch_vs_Npe[ov].Draw('same')
    latex = ROOT.TLatex(0.15,0.83,'Vov%.2f'%ov)
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextFont(42)
    latex.Draw('same')
    latexFit = ROOT.TLatex(0.15,0.73,'#sigma_{t}^{stoch} = %.0f*N_{phe}^{%.2f}'%(f_Stoch_vs_Npe[ov].GetParameter(0), f_Stoch_vs_Npe[ov].GetParameter(1)))
    latexFit.SetNDC()
    latexFit.SetTextSize(0.035)
    latexFit.SetTextFont(42)
    latexFit.Draw('same')
            
    c.SaveAs(outdir+'/'+c.GetName()+'.png')


