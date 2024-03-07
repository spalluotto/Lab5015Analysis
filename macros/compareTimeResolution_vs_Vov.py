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

xmin = 0
ymin = 0
ymax = 120


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

fnal_dir = '/eos/home-s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/plots'
may_dir = '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots'
#----- comparison ------

marker_code = True
color_code = True
specific_position = False
add_string = False

# CERN vs FNAL
if compareNum == 1:
    sipmTypes = ['HPK_nonIrr_LYSO818', 'HPK_nonIrr_LYSO818']
    nameComparison = 'HPK_nonIrr_LYSO818_Sep_vs_Mar'
    extraLabel = [' CERN',' FNAL']
    extraName = ['_angle52_T5C','_angle52_T12C']
    specific_position = True
    plots_special = ['%s'%plotsdir, '%s'%fnal_dir]
    marker_code = False
    marker_map = [20,24] 
    color_code = False
    color_map = [2, 2]


# 2E14 types
elif compareNum == 2:
    sipmTypes = ['HPK_2E14_LYSO100056', 'HPK_2E14_LYSO815', 'HPK_2E14_LYSO300032']
    nameComparison = 'HPK_2E14_angle64_T-35C_types'
    extraLabel = ['','','']
    extraName = ['_angle64_T-35C','_angle64_T-35C','_angle64_T-35C']
    color_code = False
    color_map = [417,2,1]

# 2E14 types - 1,3 only
elif compareNum == 3:
    sipmTypes = ['HPK_2E14_LYSO100056', 'HPK_2E14_LYSO300032']
    nameComparison = 'HPK_2E14_angle64_T-35C_types_1-3'
    extraLabel = ['','']
    extraName = ['_angle64_T-35C','_angle64_T-35C']
    color_code = False
    color_map = [417,1]


# non irr types
elif compareNum == 4:
    sipmTypes = ['HPK_nonIrr_LYSO818', 'HPK_nonIrr_LYSO813', 'HPK_nonIrr_LYSO816']
    nameComparison = 'HPK_nonIrr_angle64_T5C_types'
    extraLabel = ['','','']
    extraName = ['_angle64_T5C', '_angle64_T5C', '_angle64_T5C']
    color_code = False
    color_map = [417,2,1]

# non irr sipm cell sizes 
elif compareNum == 5:
    sipmTypes = ['HPK_nonIrr_LYSO820', 'HPK_nonIrr_LYSO813', 'HPK_nonIrr_LYSO814', 'HPK_nonIrr_LYSO528']
    nameComparison = 'HPK_nonIrr_angle52_cellSizes_withFNAL'
    extraLabel = ['', '', '  FNAL', '']
    extraName = ['_angle52_T5C', '_angle52_T5C', '_angle52_T12C', '_angle52_T5C']
    specific_position = True
    plots_special = ['%s'%plotsdir, '%s'%plotsdir, '%s'%fnal_dir, '%s'%plotsdir]

elif compareNum == 6:
    sipmTypes = ['HPK_nonIrr_LYSO820', 'HPK_nonIrr_LYSO813', 'HPK_nonIrr_LYSO528']
    nameComparison = 'HPK_nonIrr_angle52_T5C_cellSizes'
    extraLabel = ['', '', '']
    extraName = ['_angle52_T5C', '_angle52_T5C', '_angle52_T5C']

# 2E14 sipm cell sizes
# T-35C
elif compareNum == 7:
    sipmTypes = ['HPK_2E14_LYSO200104', 'HPK_2E14_LYSO815', 'HPK_2E14_LYSO825']
    nameComparison = 'HPK_2E14_angle52_T-35C_cellSizes'
    extraLabel = ['', '', '']
    extraName = ['_angle52_T-35C', '_angle52_T-35C', '_angle52_T-35C']

# T-30C
elif compareNum == 8:
    sipmTypes = ['HPK_2E14_LYSO200104', 'HPK_2E14_LYSO815', 'HPK_2E14_LYSO825']
    nameComparison = 'HPK_2E14_angle52_T-30C_cellSizes'
    extraLabel = ['', '', '']
    extraName = ['_angle52_T-30C', '_angle52_T-30C', '_angle52_T-30C']
# T-40C
elif compareNum == 9:
    sipmTypes = ['HPK_2E14_LYSO200104', 'HPK_2E14_LYSO815', 'HPK_2E14_LYSO825']
    nameComparison = 'HPK_2E14_angle52_T-40C_cellSizes'
    extraLabel = ['', '', '']
    extraName = ['_angle52_T-40C', '_angle52_T-40C', '_angle52_T-40C']





elif compareNum == 10:
    sipmTypes = ['HPK_2E14_LYSO100056', 'HPK_2E14_LYSO100056','HPK_2E14_LYSO100056']
    nameComparison = 'HPK_2E14_LYSO100056_T-35C_angles'
    extraLabel = [' 32^{o}', ' 52^{o}',' 64^{o}']
    extraName = ['_angle32_T-35C', '_angle52_T-35C', '_angle64_T-35C']




# non irr types
elif compareNum == 11:
    sipmTypes = ['HPK_nonIrr_LYSO818', 'HPK_nonIrr_LYSO813', 'HPK_nonIrr_LYSO816','HPK_nonIrr_LYSO818', 'HPK_nonIrr_LYSO813']
    nameComparison = 'HPK_nonIrr_angle64_T5C_types_withFNAL'
    extraLabel = ['','','',' FNAL',' FNAL']
    extraName = ['_angle64_T5C', '_angle64_T5C', '_angle64_T5C', '_angle64_T12C', '_angle64_T12C']
    color_code = False
    color_map = [417,2,1,417,2,1]
    marker_code = False
    marker_map = [20,20,20,24,24,24]
    specific_position = True
    plots_special = [ '%s'%plotsdir, '%s'%plotsdir, '%s'%plotsdir, '%s'%fnal_dir, '%s'%fnal_dir,'%s'%fnal_dir]


# 818 T1 non irr 
elif compareNum == 12:
    sipmTypes = ['HPK_nonIrr_LYSO818', 'HPK_nonIrr_LYSO818', 'HPK_nonIrr_LYSO818']
    nameComparison = 'HPK_nonIrr_LYSO818_T5C_angles'
    extraLabel = [' 32^{o}',' 52^{o}', ' 64^{o}']
    extraName = ['_angle32_T5C', '_angle52_T5C','_angle64_T5C',]






# CERN vs FNAL
elif compareNum == 20:
    sipmTypes = ['HPK_nonIrr_LYSO818', 'HPK_nonIrr_LYSO818','HPK_nonIrr_LYSO813','HPK_nonIrr_LYSO813','HPK_nonIrr_LYSO528','HPK_nonIrr_LYSO528']
    nameComparison = 'HPK_nonIrr_Sep_vs_Mar'
    extraLabel = [' CERN',' FNAL',' CERN',' FNAL',' CERN',' FNAL']
    extraName = ['_angle52_T5C','_angle52_T12C','_angle52_T5C','_angle52_T12C','_angle52_T5C','_angle52_T12C']
    specific_position = True
    plots_special = ['%s'%plotsdir, '%s'%fnal_dir, '%s'%plotsdir, '%s'%fnal_dir, '%s'%plotsdir, '%s'%fnal_dir]
    marker_code = False
    marker_map = [20,24, 20,24, 20,24] 
    color_code = False
    color_map = [2,2, 8,8, 4,4 ]



# CERN may vs sep
elif compareNum == 21:
    sipmTypes = ['HPK_nonIrr_LYSO820', 'HPK_nonIrr_LYSO820','HPK_nonIrr_LYSO813','HPK_nonIrr_LYSO813']
    nameComparison = 'HPK_nonIrr_Sep_vs_May'
    extraLabel = [' Sep',' May',' Sep',' May']
    extraName = ['_angle52_T5C','_angle52_T5C','_angle52_T5C','_angle52_T5C']
    specific_position = True
    plots_special = ['%s'%plotsdir, '%s'%may_dir, '%s'%plotsdir, '%s'%may_dir]
    marker_code = False
    marker_map = [20,24, 20,24] 
    color_code = False
    color_map = [2,2, 8,8]
    add_string = True 
    add_str = ['','_may','','_may']


# CERN may vs sep
elif compareNum == 22:
    sipmTypes = ['HPK_nonIrr_LYSO813', 'HPK_nonIrr_LYSO813','HPK_nonIrr_LYSO813']
    nameComparison = 'HPK_nonIrr_fnal_vs_cernMay_vs_cernSep'
    extraLabel = [' Mar',' May',' Sep']
    extraName = ['_angle52_T12C','_angle52_T5C','_angle52_T5C']
    specific_position = True
    plots_special = ['%s'%fnal_dir, '%s'%plotsdir, '%s'%may_dir]
    marker_code = False
    marker_map = [20,24,26] 
    color_code = False
    color_map = [2,4,8]
    add_string = True 
    add_str = ['','_may','','']

#-----------------------



if 'nonIrr' in nameComparison:
    xmax = 4
elif 'E1' in nameComparison:
    xmax = 1.8
else:
    xmax = 4
    

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
    if add_string:
        sipmTypes[it] = sipm + extraName[it] + add_str[it]

print(sipmTypes)
#---------



fnames = {}
labels = {}
colors = {}
markers = {}

for it, sipm in enumerate(sipmTypes):
    if specific_position:
        if add_string and add_str[it] != '':
                fnames[sipm] = '%s/summaryPlots_%s.root'%(plots_special[it], sipm.split(add_str[it])[0])
        else:
            fnames[sipm] = '%s/summaryPlots_%s.root'%(plots_special[it], sipm)
    else:
        fnames[sipm] = '%s/summaryPlots_%s.root'%(plotsdir,sipm)
    labels[sipm] = label_(sipm) + extraLabel[it]

    print('sipm : ', sipm, '     label: ', label_(sipm))
    colors[sipm] = color_map[it]
    markers[sipm] = marker_map[it]

print(fnames)
g = {}
Vovs = {}
#--- retrieve plot tRes vs bar and compute average -----
for j,sipm in enumerate(sipmTypes):
    print('\n\nsipm : ', sipm)
    f = ROOT.TFile.Open(fnames[sipm])
    print('opening file: ', fnames[sipm])
    g[sipm] = ROOT.TGraphErrors()
    Vovs[sipm] = []
    listOfKeys = [key.GetName().replace('g_deltaT_energyRatioCorr_bestTh_vs_bar_','') for key in ROOT.gDirectory.GetListOfKeys() if key.GetName().startswith('g_deltaT_energyRatioCorr_bestTh_vs_bar_')]
    for k in listOfKeys:
        Vovs[sipm].append( float (k[3:7]) )
    Vovs[sipm].sort()    
    print(sipm, Vovs[sipm])
    for i,vov in enumerate(Vovs[sipm]):
        print('\nov:  ', vov)
        gg = f.Get('g_deltaT_totRatioCorr_bestTh_vs_bar_Vov%.02f_enBin01'%(vov))
        fitFun = ROOT.TF1('fitFun','pol0',0,16)
        if not gg:
            continue
        gg.Fit(fitFun,'QR')
        print('values :    ', Vovs_eff(sipm,vov), fitFun.GetParameter(0))

        g[sipm].SetPoint(g[sipm].GetN(), Vovs_eff(sipm,vov), fitFun.GetParameter(0))
        g[sipm].SetPointError( g[sipm].GetN()-1, 0, gg.GetRMS(2) )# use RMS as error on the points
        

print('\ndraw plots')

# --- draw tRes vs vov ----
c1 =  ROOT.TCanvas('c_timeResolution_bestTh_vs_Vov','c_timeResolution_bestTh_vs_Vov',600,500)
#c1.SetGridx()
#c1.SetGridy()
ROOT.gPad.SetTicks(1)
c1.cd()
jsipm= 1
if len(sipmTypes)==1: jsipm = 0 
n = g[sipmTypes[jsipm]].GetN()

hdummy = ROOT.TH2F('hdummy','',100,xmin,xmax,100,ymin,ymax)
hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
hdummy.Draw()
leg = ROOT.TLegend(0.15,0.70,0.90,0.92)
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
    leg.AddEntry( g[sipm], labels[sipm], 'Pl')
leg.Draw('same')

cms_logo = draw_logo()
cms_logo.Draw()    

c1.SaveAs(outdir+c1.GetName()+'_%s.png'%nameComparison)

print('saving in ', outdir, '   as ', c1.GetName(), '_', nameComparison)


for sipm in sipmTypes:
    outFile.cd()
    g[sipm].Write('g_%s'%sipm)
outFile.Close()

    
#raw_input('OK?')
