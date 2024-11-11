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
meas = True
verbose = False
# -------------

print("\n USING STOCH MEASURED ? ", meas)

stochPow = 0.73
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
if compareNum == 1:  # USE FILES FROM SIMONA
    nameComparison = 'HPK_cellSizes'    # taking the first string before _ as label for plot
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

    ymax = 160.
    ymin = 0.
    

elif compareNum == 2: 
    nameComparison = 'HPK_types'
    pars = ['T1', 'T2', 'T3']
    pars_to_scale = pars
    angle_true = 61

    fnames = { 'T1' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle64_T5C_types.root',
               'T2' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle64_T5C_types.root',
               'T3' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle64_T5C_types.root'
               }

    labels = { 'T1' : 'HPK_nonIrr_LYSO818_angle64_T5C',
               'T2' : 'HPK_nonIrr_LYSO813_angle64_T5C',
               'T3' : 'HPK_nonIrr_LYSO816_angle64_T5C'
              }
    label_on_top = 'HPK, 25 #mum'
    plotAttrs = { 
                  'T1' : [20, ROOT.kGreen+2,  'type 1'],
                  'T2' : [21, ROOT.kBlue,     'type 2'],
                  'T3' : [22, ROOT.kRed,      'type 3']}
    ymax = 80.



elif compareNum == 3: 
    nameComparison = 'HPK_angles'
    pars = ['32', '52', '64']
    pars_to_scale = pars
    angle_true = [29, 49, 61]

    fnames = { '32' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_LYSO818_T5C_angles.root',
               '52' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_LYSO818_T5C_angles.root',
               '64' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_LYSO818_T5C_angles.root'
               }

    labels = { '32' : 'HPK_nonIrr_LYSO818_angle32_T5C',
               '52' : 'HPK_nonIrr_LYSO818_angle52_T5C',
               '64' : 'HPK_nonIrr_LYSO818_angle64_T5C'
              }
    label_on_top = 'HPK, 25 #mum'

    plotAttrs = { 
                  '32' : [20, ROOT.kGreen+2,  '32^{o}'],
                  '52' : [21, ROOT.kBlue,     '52^{o}'],
                  '64' : [22, ROOT.kRed,      '64^{o}']}
    ymax = 120.
    ymin = 0.


elif compareNum == 4: 
    nameComparison = 'HPK_types_FNAL'
    tofVersion = '2x'
    pars = ['T1', 'T2', 'T3']
    pars_to_scale = pars
    angle_true = 52
    angle_offset = 12
    fnames = { 'T1' : '/eos/home-s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle52_T5C_types_FNAL.root',
               'T2' : '/eos/home-s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle52_T5C_types_FNAL.root',
               'T3' : '/eos/home-s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_angle52_T5C_types_FNAL.root'
               }

    labels = { 'T1' : 'HPK_nonIrr_LYSO818_angle52_T12C',
               'T2' : 'HPK_nonIrr_LYSO813_angle52_T12C',
               'T3' : 'HPK_nonIrr_LYSO816_angle52_T12C'
              }
    label_on_top = 'HPK, 25 #mum'
    plotAttrs = { 
                  'T1' : [20, ROOT.kGreen+2,  'type 1'],
                  'T2' : [21, ROOT.kBlue,     'type 2'],
                  'T3' : [22, ROOT.kRed,      'type 3']}
    ymax = 80.

    
    
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
    try:
        f[par] = ROOT.TFile.Open(fnames[par])
        if not f[par]:
            print(fnames[par])
            raise FileNotFoundError("File not found")
        g[par] = f[par].Get('g_data_vs_Vov_average_%s'%labels[par])
        if not g[par]:
            print('g_data_vs_Vov_average_',labels[par],'  not found in  ', fnames[par])
            raise AttributeError("Graph not found in file")

    except (FileNotFoundError, AttributeError) as e:
        print(f"Error: {e}")
    g_scaled[par] = ROOT.TGraphErrors()
    g_scaled[par].SetName('g_data_scaled_vs_Vov_average_%s'%labels[par]) 

    g_scaledMeas[par] = ROOT.TGraphErrors()
    g_scaledMeas[par].SetName('g_dataMeas_scaled_vs_Vov_average_%s'%labels[par]) 

    
# scale (2C) to take into account angle offset in 2023 Sep TB 
for par in pars_to_scale:
    print("\n ", par)
    if par not in pars_to_scale: continue
    g_Noise[par] = f[par].Get('g_Noise_vs_Vov_average_%s'%labels[par])
    g_Stoch[par] = f[par].Get('g_Stoch_vs_Vov_average_%s'%labels[par])
    g_StochMeas[par] = f[par].Get('g_StochMeas_vs_Vov_average_%s'%labels[par])
    g_SR[par]   = f[par].Get('g_SR_vs_Vov_average_%s'%labels[par])
    for i in range(0, g[par].GetN()):
        vov = g[par].GetX()[i]
        #s_noise = g_Noise[par].Eval(vov)/enScale[par]
        sr = g_SR[par].GetY()[i]
        err_sr = g_SR[par].GetEY()[i]
        s_noise,err_s_noise =  sigma_noise(sr*enScale[par], tofVersion, err_sr*enScale[par])

        s_stoch = g_Stoch[par].GetY()[i]/math.pow(enScale[par], stochPow)
        err_s_stoch = g_Stoch[par].GetEY()[i]/math.pow(enScale[par], stochPow)
        
        s_stochMeas = g_StochMeas[par].GetY()[i]/math.pow(enScale[par], stochPow)
        err_s_stochMeas = g_StochMeas[par].GetEY()[i]/math.pow(enScale[par], stochPow)
        
        s_dcr = 0.
        err_s_dcr = 0.

        s_tot = math.sqrt(s_noise*s_noise + s_stoch*s_stoch + s_dcr*s_dcr)
        #err_s_tot = 1/s_tot * math.sqrt(math.pow(s_noise*err_s_noise,2) + math.pow(s_stoch*err_s_stoch,2) + math.pow(s_dcr*err_s_dcr,2))
        err_s_tot = g[par].GetEY()[i]
        
        s_totMeas = math.sqrt(s_noise*s_noise + s_stochMeas*s_stochMeas + s_dcr*s_dcr)
        #err_s_totMeas = 1/s_totMeas * math.sqrt(math.pow(s_noise*err_s_noise,2) + math.pow(s_stochMeas*err_s_stochMeas,2) + math.pow(s_dcr*err_s_dcr,2))
        err_s_totMeas = g[par].GetEY()[i]

        g_scaled[par].SetPoint(i, vov, s_tot) # correct for angle offset 
        g_scaled[par].SetPointError(i, 0, err_s_tot) # correct for angle offset

        g_scaledMeas[par].SetPoint(i, vov, s_totMeas) # correct for angle offset 
        g_scaledMeas[par].SetPointError(i, 0, err_s_totMeas) # correct for angle offset

        print("ov : ", vov, "\t data scaled : ", round(s_totMeas,2))
        if verbose:
            print("OV : ", vov)
            print("scaling -- > ", round(enScale[par],2))
            print("data : ",round(g[par].GetY()[i],1), "tot scaled : ", round(s_tot,1), " ---- noise true : ", round(sigma_noise(sr,tofVersion,err_sr)[0],1), "  noise scaled: ", round(s_noise,1), "  stoch true ", round(g_Stoch[par].Eval(vov),1), "  stoch scaled ", round(s_stoch,1), "  stoch meas true : ", round(s_stochMeas,1))
            print("err on stoch : ", err_s_stochMeas)

            
            

g_uff={}
if meas:
    g_uff = g_scaledMeas.copy()
else:
    g_uff = g_scaled.copy()

if verbose:
    print(meas)
    for par in pars_to_scale:
        for i in range(g_scaled[par].GetN()):
            print("\n \n      meas  ", g_scaledMeas[par].GetY()[i], "    exp  ", g_scaled[par].GetY()[i], "    uff  ", g_uff[par].GetY()[i])    


# plot    
leg = ROOT.TLegend(0.70, 0.60, 0.89, 0.89)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045) 


c = ROOT.TCanvas('c_timeResolution_%s_nonIrr_vs_Vov'%nameComparison,'c_timeResolution_%s_nonIrr_vs_Vov'%nameComparison, 600, 500)
hPad = ROOT.gPad.DrawFrame(0.,ymin,4.0,ymax)
hPad.SetTitle(";V_{OV} [V];time resolution [ps]")
hPad.Draw()
ROOT.gPad.SetTicks(1)

for par in pars:
    if par in pars_to_scale:
        g_uff[par].Sort()
        g_uff[par].SetMarkerSize(1)
        if (plotAttrs[par][0] == 22 or plotAttrs[par][0] == 23): g_uff[par].SetMarkerSize(1.15)
        g_uff[par].SetMarkerStyle(plotAttrs[par][0])
        g_uff[par].SetMarkerColor(plotAttrs[par][1])
        g_uff[par].SetLineColor(plotAttrs[par][1])
        leg.AddEntry(g_uff[par], '%s'%plotAttrs[par][2],'PL')
        g_uff[par].Draw('plsame')
    else:
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
tl.DrawLatex(0.20,0.80,'non-irradiated')

#cms_logo = draw_logo()
#cms_logo.Draw()

c.SaveAs(outdir+'%s.png'%c.GetName())
c.SaveAs(outdir+'%s.pdf'%c.GetName())


