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
import CMS_lumi, tdrstyle
from moduleDict import *
from Vovs_eff import *

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
ROOT.gStyle.SetLegendTextSize(0.040)
ROOT.gStyle.SetPadTopMargin(0.07)
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning   


outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_May23/compareTimeResolution/'


#---- init ---

compareNum = 1

#-------------

#----- comparison ------
if compareNum == 1:
    sipmTypes = ['HPK_2E14_LYSO815', 'HPK_2E14_LYSO815', 'HPK_2E14_LYSO815']
    nameComparison = 'temperatures_HPK_2E14_LYSO815'
    extraLabel = ['  -30^{o}C','  -35^{o}C','  -40^{o}C']
    extraName = ['_T-30C','_T-35','_T-40C']
    color_code = True



#-----------------------

outFile = ROOT.TFile('/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/compareTimeResolution_vs_Vov_%s.root'%nameComparison, 'RECREATE')


color_map = [850,880,800,840,910]
#color_map = [417,632,1]


#-- extra name
for it,sipm in enumerate(sipmTypes):
    sipmTypes[it] = sipm + extraName[it]

print sipmTypes
#---------



fnames = {}
labels = {}
colors = {}
markers = {}

for it, sipm in enumerate(sipmTypes):
    fnames[sipm] = '../plots/summaryPlots_%s.root'%(sipm)
    labels[sipm] = label_(sipm) + extraLabel[it]
    if not color_code:
        colors[sipm] = color_(sipm)
    else:
        colors[sipm] = color_map[it]
    markers[sipm] = 20


g = {}
Vovs = {}
#--- retrieve plot tRes vs bar and compute average -----
for j,sipm in enumerate(sipmTypes):
    f = ROOT.TFile.Open(fnames[sipm])
    g[sipm] = ROOT.TGraphErrors()
    Vovs[sipm] = []
    listOfKeys = [key.GetName().replace('g_deltaT_energyRatioCorr_bestTh_vs_bar_','') for key in ROOT.gDirectory.GetListOfKeys() if key.GetName().startswith('g_deltaT_energyRatioCorr_bestTh_vs_bar_')]
    for k in listOfKeys:
        Vovs[sipm].append( float (k[3:7]) )
    Vovs[sipm].sort()    
    print sipm, Vovs[sipm]
    for i,vov in enumerate(Vovs[sipm]):
        gg = f.Get('g_deltaT_totRatioCorr_bestTh_vs_bar_Vov%.02f_enBin01'%(vov))
        fitFun = ROOT.TF1('fitFun','pol0',0,16)
        #fitFun.SetRange(3,12)
        gg.Fit(fitFun,'QR')
        print sipm, Vovs_eff(vov,sipm), fitFun.GetParameter(0)

        g[sipm].SetPoint(g[sipm].GetN(), Vovs_eff(vov,sipm), fitFun.GetParameter(0))
        g[sipm].SetPointError( g[sipm].GetN()-1, 0, gg.GetRMS(2) )# use RMS as error on the points
        

# --- draw tRes vs vov ----
c1 =  ROOT.TCanvas('c_timeResolution_bestTh_vs_Vov','c_timeResolution_bestTh_vs_Vov',900,700)
c1.SetGridx()
c1.SetGridy()
c1.cd()
jsipm= 1
if len(sipmTypes)==1: jsipm = 0 
n = g[sipmTypes[jsipm]].GetN()
xmax = 4
xmin = 0

ymin = 0
ymax = 120

hdummy = ROOT.TH2F('hdummy','',100,xmin,xmax,100,ymin,ymax)
hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
hdummy.Draw()
leg = ROOT.TLegend(0.30,0.74,0.90,0.92)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
for i,sipm in enumerate(sipmTypes):
    g[sipm].SetMarkerSize(1)
    g[sipm].SetMarkerStyle(markers[sipm])
    g[sipm].SetMarkerColor(colors[sipm])
    g[sipm].SetLineColor(colors[sipm])
    g[sipm].SetLineStyle(1)
    g[sipm].SetLineWidth(1)
    g[sipm].Draw('plsame')
    leg.AddEntry( g[sipm], labels[sipm], 'PL')
leg.Draw('same')


# latex = ROOT.TLatex(0.65,0.68,'%s'%irr)
# if (irr == 'unirr'):
#     latex = ROOT.TLatex(0.65,0.68,'non-irradiated')
# latex.SetNDC()
# latex.SetTextSize(0.045)
# latex.SetTextFont(42)
# #latex.Draw('same')



for c in [c1]:
    c.SaveAs(outdir+c.GetName()+'_%s.png'%nameComparison)
    c.SaveAs(outdir+c.GetName()+'_%s.pdf'%nameComparison)


for sipm in sipmTypes:
    outFile.cd()
    g[sipm].Write('g_%s'%sipm)
outFile.Close()

    
#raw_input('OK?')
