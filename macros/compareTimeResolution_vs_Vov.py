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
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning

parser = argparse.ArgumentParser()  
parser.add_argument("-n","--comparisonNumber", required = True, type=str, help="comparison number")    
args = parser.parse_args()   


#---- init ---

compareNum = int(args.comparisonNumber)

#-------------

outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_May23/compareTimeResolution/'
plotsdir = '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots'
#plotsdir = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/'


#----- comparison ------

marker_code = True
color_code = True


# ----- LYSO 815 ------
if compareNum == 1:
    sipmTypes = ['HPK_2E14_LYSO815', 'HPK_2E14_LYSO815', 'HPK_2E14_LYSO815']
    nameComparison = '2E14_LYSO815_temperatures'
    extraLabel = ['','','']
    extraName = ['_angle52_T-30C','_angle52_T-35C','_angle52_T-40C']


elif compareNum == 2:
    sipmTypes = ['HPK_2E14_LYSO815', 'HPK_2E14_LYSO815', 'HPK_2E14_LYSO815']
    nameComparison = '2E14_LYSO815_angles_T-35C'
    extraLabel = [' - 32^{o}',' - 52^{o}',' - 64^{o}']
    extraName = ['_angle32_T-35C','_angle52_T-35C','_angle64_T-35C']


# ----- LYSO 825 ------
elif compareNum == 3:
    sipmTypes = ['HPK_2E14_LYSO825', 'HPK_2E14_LYSO825', 'HPK_2E14_LYSO825']
    nameComparison = '2E14_LYSO825_temperatures'
    extraLabel = ['','','']
    extraName = ['_angle52_T-30C','_angle52_T-35C','_angle52_T-40C']


elif compareNum == 4:
    sipmTypes = ['HPK_2E14_LYSO825', 'HPK_2E14_LYSO825']
    nameComparison = '2E14_LYSO825_angles_T-35C'
    extraLabel = [' - 52^{o}',' - 64^{o}']
    extraName = ['_angle52_T-35C','_angle64_T-35C']





# ---------------------
# ----- LYSO 819 ------
elif compareNum == 5:
    sipmTypes = ['HPK_1E14_LYSO819', 'HPK_1E14_LYSO819', 'HPK_1E14_LYSO819' , 'HPK_1E14_LYSO819']
    nameComparison = '1E14_LYSO819_temperatures'
    extraLabel = ['','','',   '']
    extraName = ['_angle52_T-22C','_angle52_T-27C', '_angle52_T-32C', '_angle52_T-37C'     ]

elif compareNum == 6:
    sipmTypes = ['HPK_1E14_LYSO819', 'HPK_1E14_LYSO819', 'HPK_1E14_LYSO819']
    nameComparison = '1E14_LYSO819_angles_T-22C'
    extraLabel = [' - 32^{o}',' - 52^{o}',' - 64^{o}']
    extraName = ['_angle32_T-22C','_angle52_T-22C','_angle64_T-22C']

elif compareNum == 7:
    sipmTypes = ['HPK_1E14_LYSO819', 'HPK_1E14_LYSO819', 'HPK_1E14_LYSO819']
    nameComparison = '1E14_LYSO819_angles_T-32C'
    extraLabel = [' - 32^{o}',' - 52^{o}',' - 64^{o}']
    extraName = ['_angle32_T-32C','_angle52_T-32C','_angle64_T-32C']



# ---------------------
# ----- LYSO 829 ------
elif compareNum == 8:
    sipmTypes = ['HPK_1E13_LYSO829', 'HPK_1E13_LYSO829', 'HPK_1E13_LYSO829' , 'HPK_1E13_LYSO829']
    nameComparison = '1E13_LYSO829_temperatures'
    extraLabel = ['' ,'','',   '']
    extraName = ['_angle52_T-32C','_angle52_T-19C', '_angle52_T0C', '_angle52_T12C'     ]


elif compareNum == 9:
    sipmTypes = ['HPK_1E13_LYSO829', 'HPK_1E13_LYSO829', 'HPK_1E13_LYSO829']
    nameComparison = '1E13_LYSO829_angles_T-19C'
    extraLabel = [' - 32^{o}',' - 52^{o}',' - 64^{o}']
    extraName = ['_angle32_T-19C','_angle52_T-19C','_angle64_T-19C']






#### --------   thickening scenarios ------
elif compareNum == 10:
    sipmTypes = ['HPK_1E14_LYSO819','HPK_2E14_LYSO815','HPK_1E14_LYSO817']
    nameComparison = 'T1_T2_T3_EoLemulation'
    extraLabel = [' - T1 - 32^{o}',' - T2 - 52^{o}',' - T3 - 64^{o}']
    extraName = ['_angle32_T-22C', '_angle52_T-35C', '_angle64_T-22C']
    color_code = False
    color_map = [417,2,1]



elif compareNum == 20:
    sipmTypes = ['HPK_1E14_LYSO819','HPK_2E14_LYSO815','HPK_1E14_LYSO817']
    nameComparison = 'T1_T2_T3_angle64_EoLemulation'
    extraLabel = [' - T1',          ' - T2',           ' - T3']
    extraName = ['_angle64_T-22C', '_angle64_T-35C', '_angle64_T-22C']
    color_code = False
    color_map = [417,2,1]






elif compareNum == 11:
    sipmTypes = ['HPK_1E14_LYSO819','HPK_2E14_LYSO815','HPK_2E14_LYSO815']
    nameComparison = 'T1_T2_T2_EoLemulation'
    extraLabel = [' - T1 - 32^{o}',' - T2 - 52^{o}',' - T2 - 64^{o}']
    extraName =['_angle32_T-22C', '_angle52_T-35C', '_angle64_T-35C']
    color_code = False
    color_map = [417,2,1]

elif compareNum == 12:
    sipmTypes = ['HPK_1E14_LYSO819','HPK_1E14_LYSO819','HPK_1E14_LYSO819']
    nameComparison = 'T1_T1_T1_EoLemulation'
    extraLabel = [' - T1 - 32^{o}',' - T1 - 52^{o}',' - T1 - 64^{o}']
    extraName = ['_angle32_T-22C', '_angle52_T-22C', '_angle64_T-22C']
    color_code = False
    color_map = [417,2,1]


elif compareNum == 13:
    sipmTypes = ['HPK_1E14_LYSO819','HPK_1E14_LYSO817']
    nameComparison = 'T1_T3_EoLemulation'
    extraLabel = [' - T1',' - T3']
    extraName = ['_angle64_T-22C', '_angle64_T-22C']
    color_code = False
    color_map = [417,1]








#---------- BTL like ------
elif compareNum == 14:
    sipmTypes = ['HPK_1E14_LYSO819','HPK_1E14_LYSO817']
    nameComparison = 'T1_T3_BTLlike1E14'
    extraLabel = [' - T1',' - T3']
    extraName = ['_angle64_T-32C', '_angle64_T-32C']
    color_code = False
    color_map = [417,1]


elif compareNum == 15:
    sipmTypes = ['HPK_1E14_LYSO819','HPK_2E14_LYSO815','HPK_1E14_LYSO817']
    nameComparison = 'T1_T2_T3_BTLlike1E14'
    extraLabel = [' - T1 - 32^{o}',' - T2 - 52^{o}',' - T3 - 64^{o}']
    extraName = ['_angle32_T-32C', '_angle52_T-40C', '_angle64_T-32C']
    color_code = False
    color_map = [417,2,1]


elif compareNum == 16:
    sipmTypes = ['HPK_1E14_LYSO819','HPK_2E14_LYSO815','HPK_2E14_LYSO815']
    nameComparison = 'T1_T2_T2_BTLlike1E14'
    extraLabel = [' - T1 - 32^{o}',' - T2 - 52^{o}',' - T2 - 64^{o}']
    extraName = ['_angle32_T-32C', '_angle52_T-40C', '_angle64_T-40C']
    color_code = False
    color_map = [417,2,1]


elif compareNum == 17:
    sipmTypes = ['HPK_1E14_LYSO819','HPK_1E14_LYSO819','HPK_1E14_LYSO819']
    nameComparison = 'T1_T1_T1_BTLlike1E14'
    extraLabel = [' - T1 - 32^{o}',' - T1 - 52^{o}',' - T1 - 64^{o}']
    extraName = ['_angle32_T-32C', '_angle52_T-32C', '_angle64_T-32C']
    color_code = False
    color_map = [417,2,1]








# ---- cell size ------

elif compareNum == 18:
    sipmTypes = ['HPK_2E14_LYSO825', 'HPK_2E14_LYSO825', 'HPK_2E14_LYSO825','HPK_2E14_LYSO815', 'HPK_2E14_LYSO815', 'HPK_2E14_LYSO815']
    nameComparison = '2E14_LYSO825_LYSO815_temperatures'
    extraLabel = ['','','','','','']
    extraName = ['_angle52_T-30C','_angle52_T-35C','_angle52_T-40C','_angle52_T-30C','_angle52_T-35C','_angle52_T-40C']
    marker_code = False
    marker_map = [24,24,24,20,20,20]
    color_code = False
    color_map = [2,800,860,2,800,860]




elif compareNum == 19:
    sipmTypes = ['HPK_2E14_LYSO825', 'HPK_2E14_LYSO815']
    nameComparison = '2E14_cellSize_EoLemulation'
    extraLabel = ['','']
    extraName = ['_angle52_T-35C','_angle52_T-35C']



# ---- T1 EoL emulation ----
elif compareNum == 21:
    sipmTypes = ['HPK_1E14_LYSO819', 'HPK_1E13_LYSO829']
    nameComparison = 'HPK_T1_EoLemulation'
    extraLabel = ['','']
    extraName = ['_angle52_T-22C','_angle52_T12C']





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
        g[sipm].SetPointError( g[sipm].GetN()-1, 0, gg.GetRMS(2) )# use RMS as error on the points
        

print '\ndraw plots'

# --- draw tRes vs vov ----
c1 =  ROOT.TCanvas('c_timeResolution_bestTh_vs_Vov','c_timeResolution_bestTh_vs_Vov',600,500)
c1.cd()
jsipm= 1
if len(sipmTypes)==1: jsipm = 0 
n = g[sipmTypes[jsipm]].GetN()
xmax = 4
xmin = 0

ymin = 0
ymax = 120

hdummy = ROOT.TH2F('hdummy','',100,xmin,xmax,100,ymin,ymax)
hdummy.GetXaxis().SetTitle('V_{OV} [V]')
hdummy.GetYaxis().SetTitle('time resolution [ps]')
hdummy.Draw()
ROOT.gPad.SetTicks(1)

leg = ROOT.TLegend(0.40,0.65,0.90,0.92)
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
