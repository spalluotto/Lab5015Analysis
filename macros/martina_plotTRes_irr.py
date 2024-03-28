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
ROOT.gStyle.SetPadRightMargin(0.07)
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning






# ---- EDIT ---- 
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'
angle_offset = 3
# -------------

srScale = 1.20 # scaling SR from TOFHIR2X to 2C


parser = argparse.ArgumentParser()  
parser.add_argument("-n","--comparisonNumber", required = True, type=str, help="comparison number")    
args = parser.parse_args()   


#---- init ---
compareNum = int(args.comparisonNumber)



fnames = {}
gnames = {}
labels = {}

irr_label = '2 #times 10^{14} 1 MeV n_{eq}/cm^{2}'

# cell sizes
if compareNum == 1:
    nameComparison = 'HPK_2E14_cellSizes'
    pars = [20, 25, 30]
    pars_to_scale = pars
    angle_true = 49

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
    ymax = 120.

    
# types
elif compareNum == 2:
    nameComparison = 'HPK_2E14_types'
    pars = ['T1', 'T2', 'T3']
    pars_to_scale = pars
    angle_true = 61

    fnames = { 'T1' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_T-35C_angle64_types.root',
               'T2' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_T-35C_angle64_types.root',
               'T3' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_T-35C_angle64_types.root'
               }

    labels = { 'T1' : 'HPK_2E14_LYSO100056_angle64_T-35C',
               'T2' : 'HPK_2E14_LYSO815_angle64_T-35C',
               'T3' : 'HPK_2E14_LYSO300032_angle64_T-35C'
              }

    plotAttrs = {
                  'T1' : [20, ROOT.kGreen+2,  'type 1'],
                  'T2' : [21, ROOT.kBlue,     'type 2'],
                  'T3' : [22, ROOT.kRed,      'type 3']}
    ymax = 120.


# angles
elif compareNum == 3:
    nameComparison = 'HPK_2E14_angles'
    pars = ['32', '52', '64']
    pars_to_scale = pars
    angle_true = [29, 49, 61]
    fnames = { '32' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_T-35C_angles.root',
               '52' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_T-35C_angles.root',
               '64' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_T-35C_angles.root'
              }
    labels = { '32' : 'HPK_2E14_LYSO100056_angle32_T-35C',
               '52' : 'HPK_2E14_LYSO100056_angle52_T-35C',
               '64' : 'HPK_2E14_LYSO100056_angle64_T-35C'
              }

    plotAttrs = { 
                  '32' : [20, ROOT.kGreen+2,  '32^{o}'],
                  '52' : [21, ROOT.kBlue,     '52^{o}'],
                  '64' : [22, ROOT.kRed,      '64^{o}']}
    ymax = 120.




# TYPE 1 - irradiated 2E14 - temperatures comparison
elif compareNum == 4:
    nameComparison = 'HPK_2E14_T1_temperatures'
    pars = ['-40', '-35', '-30']
    pars_to_scale = pars
    angle_true = 49
    fnames = { '-40' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_temperatures.root',
               '-35' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_temperatures.root',
               '-30' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_temperatures.root'
              }
    labels = { '-40' : 'HPK_2E14_LYSO100056_angle52_T-40C',
               '-35' : 'HPK_2E14_LYSO100056_angle52_T-35C',
               '-30' : 'HPK_2E14_LYSO100056_angle52_T-30C'
              }
    plotAttrs = { 
                  '-40' : [20, ROOT.kGreen+2,  '-40^{o}C'],
                  '-35' : [21, ROOT.kBlue,     '-35^{o}C'],
                  '-30' : [22, ROOT.kRed,      '-30^{o}C']
                 }
    ymax = 120.



# TYPE 1 - irradiated 1E14 - temperatures comparison
elif compareNum == 5:
    nameComparison = 'HPK_1E14_T1_temperatures'
    pars = ['-37', '-32', '-27']
    pars_to_scale = pars
    angle_true = 49
    irr_label = '1 #times 10^{14} 1 MeV n_{eq}/cm^{2}'
    fnames = { '-37' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_1E14_LYSO819_temperatures.root',
               '-32' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_1E14_LYSO819_temperatures.root',
               '-27' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_1E14_LYSO819_temperatures.root'
              }
    labels = { '-37' : 'HPK_1E14_LYSO819_angle52_T-37C',
               '-32' : 'HPK_1E14_LYSO819_angle52_T-32C',
               '-27' : 'HPK_1E14_LYSO819_angle52_T-27C'
              }
    plotAttrs = { 
                  '-37' : [20, ROOT.kGreen+2,  '-37^{o}C'],
                  '-32' : [21, ROOT.kBlue,     '-32^{o}C'],
                  '-27' : [22, ROOT.kRed,      '-27^{o}C']
                 }
    ymax = 120.


    
    
# energy scaling for angle offset
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
g_Noise = {}
g_Stoch = {}
g_DCR = {}
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
    

# # scale 15 um 2X --> 2C
# if compareNum == 1:
#     g_Noise[15] = f[15].Get('g_Noise_vs_Vov_average_%s'%labels[15])
#     g_Stoch[15] = f[15].Get('g_Stoch_vs_Vov_average_%s'%labels[15])
#     g_DCR[15]   = f[15].Get('g_DCR_vs_Vov_average_%s'%labels[15])
#     g_SR[15]    = f[15].Get('g_SR_vs_Vov_average_%s'%labels[15])
    
#     for i in range(0, g[15].GetN()):
#         vov = g[15].GetX()[i]
#         sr = g_SR[15].Eval(vov)
#         s_noise_scaled = sigma_noise(sr*srScale, '2C')
#         s_stoch = g_Stoch[15].Eval(vov)
#         s_dcr = g_DCR[15].Eval(vov)
#         s_tot = math.sqrt(s_noise_scaled*s_noise_scaled + s_stoch*s_stoch + s_dcr*s_dcr)
#         g_scaled[15].SetPoint(i, vov, s_tot)
#         g_scaled[15].SetPointError(i, 0, g[15].GetErrorY(i))


# scale others (2C) to take into account angle offset in 2023 Sep TB 
for par in pars_to_scale:
    print("\n ", par)
    if par not in pars_to_scale: continue
    g_Noise[par] = f[par].Get('g_Noise_vs_Vov_average_%s'%labels[par])
    g_Stoch[par] = f[par].Get('g_Stoch_vs_Vov_average_%s'%labels[par])
    g_SR[par]   = f[par].Get('g_SR_vs_Vov_average_%s'%labels[par])
    g_DCR[par]   = f[par].Get('g_DCR_vs_Vov_average_%s'%labels[par])

    for i in range(0, g[par].GetN()):
        vov = g[par].GetX()[i]
        #s_noise = gNoise[par].Eval(vov)/enScale[par]
        sr = g_SR[par].Eval(vov)
        s_noise =  sigma_noise(sr*enScale[par], '2c')
        s_stoch = g_Stoch[par].Eval(vov)/math.sqrt(enScale[par])
        s_dcr = g_DCR[par].Eval(vov)/enScale[par]
        s_tot = math.sqrt(s_noise*s_noise + s_stoch*s_stoch + s_dcr*s_dcr)

        print("tot : ", s_tot, " ---- noise true : ", sigma_noise(sr,"2c"), "  noise scaled: ", s_noise, "  stoch true ", g_Stoch[par].Eval(vov), "  stoch scaled ", s_stoch, ' dcr true : ', g_DCR[par].Eval(vov), ' dcr scaled : ', s_dcr)

        g_scaled[par].SetPoint(i, vov, s_tot) # correct for angle offset
        g_scaled[par].SetPointError(i, 0, g[par].GetErrorY(i)/enScale[par]) # correct for angle offset                            
# plot
leg = ROOT.TLegend(0.60, 0.60, 0.89, 0.89)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045) 

c = ROOT.TCanvas('c_timeResolution_%s_2E14_vs_Vov'%nameComparison,'c_timeResolution_%s_2E14_vs_Vov'%nameComparison, 600, 500)
hPad = ROOT.gPad.DrawFrame(0.,20.,2.0,ymax)
hPad.SetTitle(";V_{OV} [V];time resolution [ps]")
hPad.Draw()
ROOT.gPad.SetTicks(1)
for par in pars:
    g_scaled[par].SetMarkerSize(1)
    if (plotAttrs[par][0] == 22 or plotAttrs[par][0] == 23): g_scaled[par].SetMarkerSize(1.15)
    g_scaled[par].SetMarkerStyle(plotAttrs[par][0])
    g_scaled[par].SetMarkerColor(plotAttrs[par][1])
    g_scaled[par].SetLineColor(plotAttrs[par][1])
    leg.AddEntry(g_scaled[par], '%s'%plotAttrs[par][2],'PL')

    g[par].SetMarkerStyle(plotAttrs[par][0])
    g[par].SetMarkerColor(plotAttrs[par][1])
    g[par].SetMarkerSize(1.15)
    g[par].SetLineColor(plotAttrs[par][1])
    g[par].SetLineWidth(1)
    if par in pars_to_scale:
        g_scaled[par].Draw('plsame')
    else:
        g[par].Draw('plsame')
leg.Draw()

tl2 = ROOT.TLatex()
tl2.SetNDC()
tl2.SetTextFont(42)
tl2.SetTextSize(0.045)
tl2.DrawLatex(0.20,0.20,'%s'%nameComparison.split('_')[0])

tl = ROOT.TLatex()
tl.SetNDC()
tl.SetTextFont(42)
tl.SetTextSize(0.045)
tl.DrawLatex(0.58,0.20, irr_label)

cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'%s.png'%c.GetName())
c.SaveAs(outdir+'%s.pdf'%c.GetName())


# outfile   = ROOT.TFile.Open(outdir+'/%s.root'%c.GetName(),'recreate')
# for par in pars:
#     outfile.cd()
#     g_scaled[par].Write(g_scaled[par].GetName())
