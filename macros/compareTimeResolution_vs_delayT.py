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

webdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/'

outdir = '%s/compareTimeResolution/'%webdir

#----- comparison ------
nameComparison = 'delayTscan_HPK_2E14_LYSO100056_T-40C'
labels         = ['0b00000111', '0b00011111', '0b01111111', '0b10000001', '0b10000111', '0b10011111', '0b11111111', '0b00000111']
#-----------------------

sipmTyps = []
for l in labels:
    sipmTypes.append('HPK_2E14_LYSO100056_Vov1.25_angle51_delayT%s_T-40C'%l)


fnames = {}
colors = {}
markers = {}

for it, sipm in enumerate(sipmTypes):
    fnames[sipm] = '%s/ModuleCharacterization/%s/summaryPlots_%s.root'%(webdir,sipm,sipm)
    colors[sipm] = it+1
    markers[sipm] = 20



# ------- tRes vs Vov 
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

        g[sipm].SetPoint(g[sipm].GetN(), vov, fitFun.GetParameter(0))
        g[sipm].SetPointError( g[sipm].GetN()-1, 0, gg.GetRMS(2) )# use RMS as error on the points




# ------- tRes vs delayT 
g_delayT = {}
Vovs = {}
#--- retrieve plot tRes vs bar and compute average -----
for j,sipm in enumerate(sipmTypes):
    f = ROOT.TFile.Open(fnames[sipm])
    g_delayT[sipm] = ROOT.TGraphErrors()
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

        print 'sipm_ ', sipm , '   delayT' , labels[j]

        g_delayT[sipm].SetPoint(g_delayT[sipm].GetN(), j, fitFun.GetParameter(0))
        g_delayT[sipm].SetPointError( g_delayT[sipm].GetN()-1, 0, gg.GetRMS(2) )# use RMS as error on the points






        

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
    leg.AddEntry( g[sipm], labels[i], 'PL')
leg.Draw('same')

c1.SaveAs(outdir+c1.GetName()+'_%s.png'%nameComparison)










# --- draw tRes vs delayT ----
c2 =  ROOT.TCanvas('c_timeResolution_bestTh_vs_delayT','c_timeResolution_bestTh_vs_delayT',900,700)
c2.SetGridx()
c2.SetGridy()
c2.cd()
jsipm= 1
if len(sipmTypes)==1: jsipm = 0 
n = g_delayT[sipmTypes[jsipm]].GetN()
xmax = 8
xmin = -1

ymin = 0
ymax = 120

hdummy = ROOT.TH2F('hdummy','',100,xmin,xmax,100,ymin,ymax)
hdummy.GetXaxis().SetTitle('zero')
hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
hdummy.Draw()
leg = ROOT.TLegend(0.30,0.72,0.90,0.92)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
for i,sipm in enumerate(sipmTypes):
    g_delayT[sipm].SetMarkerSize(1)
    g_delayT[sipm].SetMarkerStyle(markers[sipm])
    g_delayT[sipm].SetMarkerColor(colors[sipm])
    g_delayT[sipm].SetLineColor(colors[sipm])
    g_delayT[sipm].SetLineStyle(1)
    g_delayT[sipm].SetLineWidth(1)
    g_delayT[sipm].Draw('plsame')
    leg.AddEntry( g_delayT[sipm], labels[i], 'PL')
leg.Draw('same')

c2.SaveAs(outdir+c2.GetName()+'_%s.png'%nameComparison)
