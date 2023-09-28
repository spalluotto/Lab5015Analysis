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
from SiPM import *


parser = argparse.ArgumentParser()  
parser.add_argument("-n","--comparisonNumber", required = True, type=str, help="comparison number")    
args = parser.parse_args()   


#---- init ---

compareNum = int(args.comparisonNumber)

#-------------


def draw_logo():
    logo_x = 0.16
    logo = ROOT.TLatex()
    logo.SetNDC()
    logo.SetTextSize(0.045) 
    logo.SetTextFont(62)
    logo.DrawText(logo_x,0.95,'CMS') 
    logo.SetTextFont(52)
    logo.DrawText(logo_x+0.07, 0.95, '  Phase-2 Preliminary')
    return logo



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
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning   


outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/compareTimeResolution/'
plotsdir = '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots'
#plotsdir = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/'


#----- comparison ------

marker_code = True
color_code = True
specific_position = False

if compareNum == 1:
    sipmTypes = ['HPK_nonIrr_LYSO818', 'HPK_nonIrr_LYSO818']
    nameComparison = 'HPK_nonIrr_LYSO818_Sep_vs_Mar'
    extraLabel = [' CERN',' FNAL']
    extraName = ['_angle52_T5C','_angle52_T12C']
    specific_position = True
    plots_special = ['%s'%plotsdir, '/eos/home-s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/plots']


elif compareNum == 2:
    sipmTypes = ['HPK_2E14_LYSO100056', 'HPK_2E14_LYSO815', 'HPK_2E14_LYSO300032']
    nameComparison = 'HPK_2E14_angle64_T-35C_types'
    extraLabel = ['','','']
    extraName = ['_angle64_T-35C','_angle64_T-35C','_angle64_T-35C']
    color_code = False
    color_map = [417,2,1]


elif compareNum == 3:
    sipmTypes = ['HPK_2E14_LYSO100056', 'HPK_2E14_LYSO300032']
    nameComparison = 'HPK_2E14_angle64_T-35C_types_1-3'
    extraLabel = ['','','']
    extraName = ['_angle64_T-35C','_angle64_T-35C']
    color_code = False
    color_map = [417,1]


#-----------------------

outFile = ROOT.TFile('%s/compareTimeResolution_vs_Vov_%s.root'%(plotsdir,nameComparison), 'RECREATE')


#color_map = [850,880,800,840,910]
#color_map = [208,212,216,224,227,94,225,99,220]
if color_code:
    color_map = [2,210,4,6,7,8,94]

if marker_code:
    marker_map = [20,20,20,20,20,20,20,20]



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
    if specific_position:
        fnames[sipm] = '%s/summaryPlots_%s.root'%(plots_special[it], sipm)
    else:
        fnames[sipm] = '%s/summaryPlots_%s.root'%(plotsdir,sipm)
    labels[sipm] = label_(sipm) + extraLabel[it]

    print 'sipm : ', sipm, '     label: ', label_(sipm)
    colors[sipm] = color_map[it]
    markers[sipm] = marker_map[it]

g = {}
Vovs = {}
#--- retrieve plot tRes vs bar and compute average -----
for j,sipm in enumerate(sipmTypes):
    print '\n\nsipm : ', sipm
    f = ROOT.TFile.Open(fnames[sipm])
    print 'opening file: ', fnames[sipm]
    g[sipm] = ROOT.TGraphErrors()
    Vovs[sipm] = []
    listOfKeys = [key.GetName().replace('g_deltaT_energyRatioCorr_bestTh_vs_bar_','') for key in ROOT.gDirectory.GetListOfKeys() if key.GetName().startswith('g_deltaT_energyRatioCorr_bestTh_vs_bar_')]
    for k in listOfKeys:
        Vovs[sipm].append( float (k[3:7]) )
    Vovs[sipm].sort()    
    print sipm, Vovs[sipm]
    for i,vov in enumerate(Vovs[sipm]):
        print '\nov:  ', vov
        gg = f.Get('g_deltaT_totRatioCorr_bestTh_vs_bar_Vov%.02f_enBin01'%(vov))
        fitFun = ROOT.TF1('fitFun','pol0',0,16)
        if not gg:
            continue
        gg.Fit(fitFun,'QR')
        print 'values :    ', Vovs_eff(sipm,vov), fitFun.GetParameter(0)

        g[sipm].SetPoint(g[sipm].GetN(), Vovs_eff(sipm,vov), fitFun.GetParameter(0))
        #g[sipm].SetPointError( g[sipm].GetN()-1, 0, gg.GetRMS(2) )# use RMS as error on the points
        

print '\ndraw plots'

# --- draw tRes vs vov ----
c1 =  ROOT.TCanvas('c_timeResolution_bestTh_vs_Vov','c_timeResolution_bestTh_vs_Vov',600,500)
c1.SetGridx()
c1.SetGridy()
ROOT.gPad.SetTicks(1)
c1.cd()
jsipm= 1
if len(sipmTypes)==1: jsipm = 0 
n = g[sipmTypes[jsipm]].GetN()
xmax = 2.5
xmin = 0

ymin = 0
ymax = 120

hdummy = ROOT.TH2F('hdummy','',100,xmin,xmax,100,ymin,ymax)
hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
hdummy.Draw()
leg = ROOT.TLegend(0.15,0.74,0.90,0.92)
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

cms_logo = draw_logo()
cms_logo.Draw()    

c1.SaveAs(outdir+c1.GetName()+'_%s.png'%nameComparison)

print 'saving in ', outdir, '   as ', c1.GetName(), '_', nameComparison


for sipm in sipmTypes:
    outFile.cd()
    g[sipm].Write('g_%s'%sipm)
outFile.Close()

    
#raw_input('OK?')
