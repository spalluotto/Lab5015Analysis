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
plotsdir = '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/bkp/'

#---- init ---

compareNum = 4

#-------------

#----- comparison ------

# ----- LYSO 815 ------
if compareNum == 1:
    sipmTypes = ['HPK_2E14_LYSO815', 'HPK_2E14_LYSO815', 'HPK_2E14_LYSO815']
    nameComparison = 'HPK_2E14_LYSO815_temperatures'
    extraLabel = ['','','']
    extraName = ['_T-30C','_angle52_T-35C','_T-40C']
    color_code = True


elif compareNum == 2:
    sipmTypes = ['HPK_2E14_LYSO815', 'HPK_2E14_LYSO815', 'HPK_2E14_LYSO815']
    nameComparison = 'HPK_2E14_LYSO815_angles_T-35C'
    extraLabel = ['  32^{o}','  52^{o}','  64^{o}']
    extraName = ['_angle32_T-35C','_angle52_T-35C','_angle64_T-35C']
    color_code = True


# ----- LYSO 825 ------
elif compareNum == 3:
    sipmTypes = ['HPK_2E14_LYSO825', 'HPK_2E14_LYSO825', 'HPK_2E14_LYSO825']
    nameComparison = 'HPK_2E14_LYSO825_temperatures'
    extraLabel = ['','','']
    extraName = ['_T-30C','_angle52_T-35C','_T-40C']
    color_code = True


elif compareNum == 4:
    sipmTypes = ['HPK_2E14_LYSO825', 'HPK_2E14_LYSO825']
    nameComparison = 'HPK_2E14_LYSO825_angles_T-35C'
    extraLabel = ['  52^{o}','  64^{o}']
    extraName = ['_angle52_T-35C','_angle64_T-35C']
    color_code = True


# ---------------------
# ----- LYSO 819 ------
elif compareNum == 5:
    sipmTypes = ['HPK_1E14_LYSO819', 'HPK_1E14_LYSO819', 'HPK_1E14_LYSO819' , 'HPK_1E14_LYSO819']
    nameComparison = 'HPK_1E14_LYSO819_temperatures'
    extraLabel = ['','','',   '']
    extraName = ['_angle52_T-22C','_T-27C', '_angle52_T-32C', '_T-37C'     ]
    color_code = True

elif compareNum == 6:
    sipmTypes = ['HPK_1E14_LYSO819', 'HPK_1E14_LYSO819', 'HPK_1E14_LYSO819']
    nameComparison = 'HPK_1E14_LYSO819_angles_T-22C'
    extraLabel = ['  32^{o}','  52^{o}','  64^{o}']
    extraName = ['_angle32_T-22C','_angle52_T-22C','_angle64_T-22C']
    color_code = True

elif compareNum == 7:
    sipmTypes = ['HPK_1E14_LYSO819', 'HPK_1E14_LYSO819', 'HPK_1E14_LYSO819']
    nameComparison = 'HPK_1E14_LYSO819_angles_T-32C'
    extraLabel = ['  32^{o}','  52^{o}','  64^{o}']
    extraName = ['_angle32_T-32C','_angle52_T-32C','_angle64_T-32C']
    color_code = True


# ----- LYSO 829 ------
elif compareNum == 8:
    sipmTypes = ['HPK_1E13_LYSO829']#, 'HPK_1E13_LYSO829', 'HPK_1E13_LYSO829' , 'HPK_1E13_LYSO829']
    nameComparison = 'HPK_1E13_LYSO829_temperatures'
    extraLabel = ['']#,'','',   '']
    extraName = ['_angle52_T-19C',]#'_T-27C', '_angle52_T-32C', '_T-37C'     ]
    color_code = True



# ---- T1 for different moment of life ----

elif compareNum == 9:
    sipmTypes = ['HPK_1E13_LYSO829','HPK_1E14_LYSO819', 'HPK_1E14_LYSO819']
    nameComparison = 'diff_irrad_T1'
    extraLabel = ['','','']
    extraName = ['_angle52_T-19C','_angle52_T-22C','_angle52_T-32C'     ]
    color_code = True

#-----------------------

outFile = ROOT.TFile('%s/compareTimeResolution_vs_Vov_%s.root'%(plotsdir,nameComparison), 'RECREATE')


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
    fnames[sipm] = '%s/summaryPlots_%s.root'%(plotsdir,sipm)
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
        #fitFun.SetRange(3,12)
        if not gg:
            continue
        gg.Fit(fitFun,'QR')
        print 'values :    ', Vovs_eff(sipm,vov), fitFun.GetParameter(0)

        g[sipm].SetPoint(g[sipm].GetN(), Vovs_eff(sipm,vov), fitFun.GetParameter(0))
        g[sipm].SetPointError( g[sipm].GetN()-1, 0, gg.GetRMS(2) )# use RMS as error on the points
        

print '\ndraw plots'

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


# latex = ROOT.TLatex(0.65,0.68,'%s'%irr)
# if (irr == 'unirr'):
#     latex = ROOT.TLatex(0.65,0.68,'non-irradiated')
# latex.SetNDC()
# latex.SetTextSize(0.045)
# latex.SetTextFont(42)
# #latex.Draw('same')



c1.SaveAs(outdir+c1.GetName()+'_%s.png'%nameComparison)

print 'saving in ', outdir, '   as ', c1.GetName(), '_', nameComparison


for sipm in sipmTypes:
    outFile.cd()
    g[sipm].Write('g_%s'%sipm)
outFile.Close()

    
#raw_input('OK?')
