#! /usr/bin/env python
import os
import shutil
import glob
import math
import array
import sys
import time
import argparse
import json
import numpy as np

import ROOT
import CMS_lumi, tdrstyle
from utils import *
from SiPM import *

#set the tdr style
tdrstyle.setTDRStyle()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1)
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



# ---- EDIT ---- 
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'
angle_offset = 3
tofVersion = '2c'
# -------------



ymin = 20.
pars_to_scale = []

parser = argparse.ArgumentParser()  
parser.add_argument("-n","--comparisonNumber", required = True, type=str, help="comparison number")    
args = parser.parse_args()   


#---- init ---
compareNum = int(args.comparisonNumber)



fnames = {}
gnames = {}
labels = {}

# -- cell sizes
if compareNum == 1:
    irr_label = 'non-irradiated'
    nameComparison = 'HPK_cellSizes'
    pars = [15, 20, 25, 30]
    pars_to_scale = [15, 25, 30]
    angle_true = 49
    
    fnames = { 30 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle52_cellSizes_withFNAL.root',
               25 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle52_cellSizes_withFNAL.root',
               20 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle52_cellSizes_withFNAL.root',
               15 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle52_cellSizes_withFNAL.root'}

    labels = { 30 : 'HPK_nonIrr_LYSO820_angle52_T5C',
               25 : 'HPK_nonIrr_LYSO813_angle52_T5C',
               20 : 'HPK_nonIrr_LYSO814_angle52_T12C',
               15 : 'HPK_nonIrr_LYSO528_angle52_T5C',
              }

    label_on_top = 'HPK'
    plotAttrs = { 30 : [23, ROOT.kOrange+1, '30 #mum'],
                  25 : [20, ROOT.kGreen+2,  '25 #mum'],
                  20 : [21, ROOT.kBlue,     '20 #mum'],
                  15 : [22, ROOT.kRed,      '15 #mum']}

    ymax = 70.
    ymin = 0.

    gnames = { # name : scaling_needed, xmin, xmax, x_label, ymin, ymax, y_label]
        'Stoch_vs_PDE_average' : ['1/sqrt',0.1, 0.7, 'PDE', ymin,ymax, '#sigma_{stoch} [ps]']
    }


elif compareNum == 2:
    irr_label = '2 #times 10^{14} 1 MeV n_{eq}/cm^{2}'
    nameComparison = 'HPK_2E14_cellSizes'
    pars = [20, 25, 30]
    pars_to_scale = pars
    angle_true = 49
    label_on_top = 'HPK'

    fnames = { 30 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_T-35C_angle52_cellSize.root',
               25 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_T-35C_angle52_cellSize.root',
               20 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_T-35C_angle52_cellSize.root'
              }
    labels = { 30 : 'HPK_2E14_LYSO200104_angle52_T-35C',
               25 : 'HPK_2E14_LYSO815_angle52_T-35C',
               20 : 'HPK_2E14_LYSO825_angle52_T-35C'
              }
    plotAttrs = { 30 : [23, ROOT.kOrange+1, '30 #mum'],
                  25 : [20, ROOT.kGreen+2,  '25 #mum'],
                  20 : [21, ROOT.kBlue,     '20 #mum']
                 }

    gnames = {
    'DCR_pdescaled_vs_DCR_average' : ['1/',0, 60, 'DCR [GHz]', 0,70, '#sigma_{DCR} x PDE/PDE_{ref} [ps]']
    }


    
enScale = {}

for it,par in enumerate(pars):
    if not isinstance(angle_true, list):
        ang_true = angle_true
        angle_target = angle_true + angle_offset
    else:
        ang_true = angle_true[it]
        angle_target = angle_true[it] + angle_offset
    enScale[par] = math.cos(math.radians(ang_true)) / math.cos(math.radians(angle_target))
    



# define objects
g = {}
g_scaled = {}
g_scaledMeas = {}
g_Noise = {}
g_Stoch = {}
g_StochMeas = {}
g_SR = {}
f = {}


# retrieve files ----
for par in pars:
    g[par] = {}
    g_scaled[par] = {}
    try:
        f[par] = ROOT.TFile.Open(fnames[par])
        if not f[par]:
            print(fnames[par])
            raise FileNotFoundError("File not found")
        for graph in gnames:
            g[par][graph] = f[par].Get('g_%s_%s'%(graph, labels[par]))
            if not g[par][graph]:
                print(graph,'_',labels[par],'  not found in  ', fnames[par])
                raise AttributeError("Graph not found in file")
    except (FileNotFoundError, AttributeError) as e:
        print(f"Error: {e}")

    for graph in gnames:
        g_scaled[par][graph] = ROOT.TGraphErrors()
        g_scaled[par][graph].SetName('%s_%s'%(graph, labels[par]))


# scale Sep data to take into account angle offset in 2023 Sep TB 
for par in pars_to_scale:
    print("\n ", par)
    if par not in pars_to_scale: continue
    for graph in gnames:        
        for i in range(0, g[par][graph].GetN()):
            x = g[par][graph].GetX()[i]
            y = g[par][graph].GetY()[i]
            y_err = g[par][graph].GetErrorY(i)

            scaling = gnames[graph][0]

            if scaling == '1/sqrt':
                y_scaled = y/math.sqrt(enScale[par])
                y_err_scaled = y_err/math.sqrt(enScale[par])
            elif scaling == '1/':
                y_scaled = y/enScale[par]
                y_err_scaled = y_err/enScale[par]
            else:
                print("SCALE NOT FOUND")
                sys.exit(0)

            g_scaled[par][graph].SetPoint(i, x, y_scaled)
            g_scaled[par][graph].SetPointError(i, 0, 0)



# plot    
leg = ROOT.TLegend(0.70, 0.60, 0.89, 0.89)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045) 

for graph in gnames:
    c = ROOT.TCanvas('c_%s_%s'%(nameComparison,graph), 'c_%s_%s'%(nameComparison,graph), 600,500)

    x_min = gnames[graph][1]
    x_max = gnames[graph][2]
    y_min = gnames[graph][4]
    y_max = gnames[graph][5]

    x_lab = gnames[graph][3]
    y_lab = gnames[graph][6]

    hPad = ROOT.gPad.DrawFrame(x_min,y_min,x_max,y_max)
    hPad.SetTitle(";%s;%s"%(x_lab, y_lab))
    hPad.Draw()
    ROOT.gPad.SetTicks(1)

    if compareNum == 1 or compareNum == 2:
        mg = ROOT.TMultiGraph()
    
    for par in pars:
        if par in pars_to_scale:
            g_scaled[par][graph].Sort()
            g_scaled[par][graph].SetMarkerSize(1)
            if (plotAttrs[par][0] == 22 or plotAttrs[par][0] == 23): g_scaled[par][graph].SetMarkerSize(1.15)
            g_scaled[par][graph].SetMarkerStyle(plotAttrs[par][0])
            g_scaled[par][graph].SetMarkerColor(plotAttrs[par][1])
            g_scaled[par][graph].SetLineColor(plotAttrs[par][1])
            leg.AddEntry(g_scaled[par][graph], '%s'%plotAttrs[par][2],'PL')
            g_scaled[par][graph].Draw('plsame')
            if compareNum == 1 or compareNum==2:
                mg.Add(g_scaled[par][graph])
        else:
            g[par][graph].SetMarkerStyle(plotAttrs[par][0])
            g[par][graph].SetMarkerColor(plotAttrs[par][1])
            g[par][graph].SetMarkerSize(1.15)
            g[par][graph].SetLineColor(plotAttrs[par][1])
            g[par][graph].SetLineWidth(1)
            leg.AddEntry(g[par][graph], '%s'%plotAttrs[par][2],'PL')
            g[par][graph].Draw('plsame')
    leg.Draw()
    
    tl2 = ROOT.TLatex()
    tl2.SetNDC()
    tl2.SetTextFont(42)
    tl2.SetTextSize(0.045)
    tl2.DrawLatex(0.20,0.86,'%s'%label_on_top)
    #tl2.DrawLatex(0.20,0.86,'%s'%nameComparison.split('_')[0])

    tl = ROOT.TLatex()
    tl.SetNDC()
    tl.SetTextFont(42)
    tl.SetTextSize(0.045)
    tl.DrawLatex(0.20,0.80,'{}'.format(irr_label))


    if compareNum == 1:
        f = ROOT.TF1("", "[0]*pow(x,[1])", 0.2, 0.65)
        f.SetLineColor(1)
        f.SetLineStyle(7)
        f.SetLineWidth(1)
        mg.Fit(f, "RS+")
        f.Draw("same")
        
        lat_fit = ROOT.TLatex(0.2,0.2,"(%.1f #pm %.1f) x PDE^{(%.2f #pm %.2f)}"%(f.GetParameter(0),f.GetParError(0), f.GetParameter(1),f.GetParError(1) ) )
        lat_fit.SetNDC()
        lat_fit.SetTextSize(0.045)
        lat_fit.SetTextFont(42)
        lat_fit.Draw("same")

    elif compareNum == 2:
        f = ROOT.TF1("", "[0]*pow(x,[1])", 2, 40)
        f.SetLineColor(1)
        f.SetLineStyle(7)
        f.SetLineWidth(1)
        mg.Fit(f, "RS+")
        f.Draw("same")
        
        lat_fit = ROOT.TLatex(0.2,0.2,"(%.1f #pm %.1f) x DCR^{(%.2f #pm %.2f)}"%(f.GetParameter(0),f.GetParError(0), f.GetParameter(1),f.GetParError(1) ) )
        lat_fit.SetNDC()
        lat_fit.SetTextSize(0.045)
        lat_fit.SetTextFont(42)
        lat_fit.Draw("same")

        
    cms_logo = draw_logo()
    cms_logo.Draw()

    c.SaveAs(outdir+'%s.png'%c.GetName())
    c.SaveAs(outdir+'%s.pdf'%c.GetName())


