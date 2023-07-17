#! /usr/bin/env python

# ----- qui lo stocastico usato e quello effettivamente misurato dalla diff in quadratura, non quello scalato con pde

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
posCor = True
plotsdir = '/eos/home-s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/plots/'



# --- RUs T1 T2 T3 ----- 
if comparisonNum == 1:
    sipm = 'HPK_nonIrr_C25_LYSO816'
    outSuffix = 'scaling_%s_posCor'%sipm

    angleRef = 52
    angleDest = 64

cosRatio = math.cos(angleDest * math.pi /180 ) / math.cos(angleRef * math.pi /180 )




#--------------------------------------------------------------------------------------
sipm = sipm + '_T12C'
fname = '%s/plot_tRes_%s.root'%(plotsdir,sipm)


# ----- output --------
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_FNAL_Mar23/scaling_tRes/%s/'%outSuffix
if (os.path.exists(outdir)==False):
    os.mkdir(outdir)
#---------


graphs_t = {
    'timeResolutionAve': [1,   'data'    ,  1],
    'NoiseAve'         : [600, 'noise'   ,  cosRatio],
    'StochMeasAve'     : [418, 'stoch'   ,  math.sqrt(cosRatio)],
    'StochAve'         : [418, 'stoch'   ,  math.sqrt(cosRatio)],    
    'TotExpAve'        : [633, 'stoch #oplus noise', 1]
    }


# --- retrieve bars and ovs from plot t res

f = ROOT.TFile.Open(fname)
g_t = {}
Vovs = []
for it, graph in enumerate(graphs_t):
    g_t[graph] = f.Get('g_%s_vs_Vov'%graph)
    if it == 0:
        for ipoint in range(g_t[graph].GetN()):
            Vovs.append(g_t[graph].GetX()[ipoint])
        

#----- time resolution: splitting contributions --
g_t_scaled_vs_Vov = {}

for graph in graphs_t:
    g_t_scaled_vs_Vov[graph] = ROOT.TGraphErrors()
    if 'timeResolutionAve' in graph or 'TotExpAve' in graph: continue
    for ov in Vovs:
        if posCor:
            tmp = math.sqrt( math.pow(g_t[graph].Eval(ov),2 ) - math.pow(10 ,2) )
            g_t_scaled_vs_Vov[graph].SetPoint(g_t_scaled_vs_Vov[graph].GetN(), ov, tmp*graphs_t[graph][2])
        else:
            g_t_scaled_vs_Vov[graph].SetPoint(g_t_scaled_vs_Vov[graph].GetN(), ov, g_t[graph].Eval(ov)*graphs_t[graph][2])
        erY = 0
        for ipoint in range(g_t[graph].GetN()):
            if ov == g_t[graph].GetX()[ipoint]:
                erY = g_t[graph].GetErrorY(ipoint)
        g_t_scaled_vs_Vov[graph].SetPointError(g_t_scaled_vs_Vov[graph].GetN()-1, 0, erY)

for ov in Vovs:
    tot = math.sqrt( math.pow(g_t_scaled_vs_Vov['NoiseAve'].Eval(ov),2) + math.pow(g_t_scaled_vs_Vov['StochMeasAve'].Eval(ov),2))
    totExp = math.sqrt( math.pow(g_t_scaled_vs_Vov['NoiseAve'].Eval(ov),2) + math.pow(g_t_scaled_vs_Vov['StochAve'].Eval(ov),2))


    graph = 'timeResolutionAve'
    g_t_scaled_vs_Vov[graph].SetPoint(g_t_scaled_vs_Vov[graph].GetN(), ov, tot) 
    erY = 0
    for ipoint in range(g_t[graph].GetN()):
        if ov == g_t[graph].GetX()[ipoint]:
                erY = g_t[graph].GetErrorY(ipoint)
    g_t_scaled_vs_Vov[graph].SetPointError(g_t_scaled_vs_Vov[graph].GetN()-1, 0, erY)

    graph = 'TotExpAve'
    g_t_scaled_vs_Vov[graph].SetPoint(g_t_scaled_vs_Vov[graph].GetN(), ov, totExp) 
    erY = 0
    for ipoint in range(g_t[graph].GetN()):
        if ov == g_t[graph].GetX()[ipoint]:
                erY = g_t[graph].GetErrorY(ipoint)
    g_t_scaled_vs_Vov[graph].SetPointError(g_t_scaled_vs_Vov[graph].GetN()-1, 0, erY)




# ---- scaled -----
c = ROOT.TCanvas('c_timeResolutionScaled_vs_Vov', '', 900, 700)
c.cd()
c.SetGridy()
    
hPad = ROOT.TH2F('','',100,0,5,100,0,120)
hPad.GetXaxis().SetTitle('V_{ov} [V]')
hPad.GetYaxis().SetTitle('#sigma_{t} [ps]')
hPad.Draw()

leg = ROOT.TLegend(0.70,0.70,0.89,0.89)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
    
for it,graph in enumerate(g_t_scaled_vs_Vov):
    if 'timeResolution' in graph:
        g_t_scaled_vs_Vov[graph].SetMarkerStyle(20)
        g_t_scaled_vs_Vov[graph].SetMarkerSize(1)
        g_t_scaled_vs_Vov[graph].SetLineColor(0)
        g_t_scaled_vs_Vov[graph].SetMarkerColor(graphs_t[graph][0])
        g_t_scaled_vs_Vov[graph].Draw('epsame')
    else:
        if 'StochMeasAve' in graph :  continue
        g_t_scaled_vs_Vov[graph].SetLineColor(graphs_t[graph][0])
        g_t_scaled_vs_Vov[graph].SetFillColor(graphs_t[graph][0])
        g_t_scaled_vs_Vov[graph].SetFillColorAlpha(graphs_t[graph][0], 0.5)
        g_t_scaled_vs_Vov[graph].SetFillStyle(3001)
        g_t_scaled_vs_Vov[graph].SetLineWidth(2)
        g_t_scaled_vs_Vov[graph].Draw('E3lsame')

    leg.AddEntry(g_t_scaled_vs_Vov[graph], '%s'%graphs_t[graph][1], 'pl')
leg.Draw('same')

c.SaveAs(outdir+'/'+c.GetName()+'.png')


outFile = ROOT.TFile('%s/compareTimeResolution_vs_Vov_%s.root'%(plotsdir,outSuffix), 'RECREATE')
outFile.cd()
g_t_scaled_vs_Vov['timeResolutionAve'].Write('g_%s'%sipm)
outFile.Close()
