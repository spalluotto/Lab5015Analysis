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
verbose = False
# -------------

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
    pars = [15,20,25,30]
    nameComparison = 'HPK_nonIrr_cellsizes_bestTh_vs_Vov'

    
    plotName = 'bestTh_vs_Vov_average'
    fnames = { 30 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle52_cellSizes_withFNAL.root',
               25 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle52_cellSizes_withFNAL.root',
	       20 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle52_cellSizes_withFNAL.root',
               15 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle52_cellSizes_withFNAL.root'}

    labels = { 30 : 'HPK_nonIrr_LYSO820_angle52_T5C',
               25 : 'HPK_nonIrr_LYSO813_angle52_T5C',
               20 : 'HPK_nonIrr_LYSO814_angle52_T12C',
               15 : 'HPK_nonIrr_LYSO528_angle52_T5C',
              }

    # plot settings
    plotAttrs = { 30 : [23, ROOT.kOrange+1, '30 #mum'],
                  25 : [20, ROOT.kGreen+2,  '25 #mum'],
                  20 : [21, ROOT.kBlue,     '20 #mum'],
                  15 : [22, ROOT.kRed,      '15 #mum']}
    label_on_top = 'HPK'
    irr_label = 'non-irradiated'
    x_label = 'V_{OV} [V]'
    y_label = 'timing threshold [DAC]'
    ymax = 50.
    ymin = 0.




# define objects
g = {}
f = {}

# retrieve files ----
for par in pars:
    try:
        f[par] = ROOT.TFile.Open(fnames[par])
        if not f[par]:
            print(fnames[par])
            raise FileNotFoundError("File not found")
        g[par] = f[par].Get('g_%s_%s'%(plotName, labels[par]))
        if not g[par]:
            print('g_',plotName,'_average_',labels[par],'  not found in  ', fnames[par])
            raise AttributeError("Graph not found in file")

    except (FileNotFoundError, AttributeError) as e:
        print(f"Error: {e}")
    
# plot    
leg = ROOT.TLegend(0.70, 0.60, 0.89, 0.89)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045) 

c = ROOT.TCanvas('c_%s'%nameComparison,'c_%s'%nameComparison, 600, 500)
hPad = ROOT.gPad.DrawFrame(0.,ymin,4.0,ymax)
hPad.SetTitle(";%s;%s"%(x_label, y_label))
hPad.Draw()
ROOT.gPad.SetTicks(1)

for par in pars:
    g[par].SetMarkerStyle(plotAttrs[par][0])
    g[par].SetMarkerColor(plotAttrs[par][1])
    g[par].SetMarkerSize(1.15)
    g[par].SetLineColor(plotAttrs[par][1])
    g[par].SetLineWidth(1)
    leg.AddEntry(g[par], '%s'%plotAttrs[par][2],'PL')
    g[par].Draw('plsame')
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
tl.DrawLatex(0.20,0.80,'%s'%irr_label)

#cms_logo = draw_logo()
#cms_logo.Draw()

c.SaveAs(outdir+'%s.png'%c.GetName())
c.SaveAs(outdir+'%s.pdf'%c.GetName())


