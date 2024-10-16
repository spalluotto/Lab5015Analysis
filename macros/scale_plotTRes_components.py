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
ROOT.gStyle.SetPadRightMargin(0.05)
ROOT.gStyle.SetPadTopMargin(0.07)
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning


# ---- EDIT ---- 
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/components/'
angle_offset = 3
pars_to_scale = []
# -------------

stochPow = 0.73


#---- init ---
parser = argparse.ArgumentParser()  
parser.add_argument("-n","--comparisonNumber", required = True, type=str, help="comparison number")    
args = parser.parse_args()   

compareNum = int(args.comparisonNumber)


fnames = {}
gnames = {}
labels = {}

ymin = 0.
ymax = 100
xmax = 4.
xmin = 0.

# non irr cell sizes
if compareNum == 2:
    nameComparison = 'nonIrr_cellSizes'
    irr_label = 'non irradiated'
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

    plotAttrs = { 30 : [23, ROOT.kOrange+1, '30 #mum'],
                  25 : [20, ROOT.kGreen+2,  '25 #mum'],
                  20 : [21, ROOT.kBlue,     '20 #mum'],
                  15 : [22, ROOT.kRed,      '15 #mum']}

    ymax = 160.



# non irr types
elif compareNum == 3:
    nameComparison = 'nonIrr_types'
    irr_label = 'non irradiated'
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

    plotAttrs = { 
                  'T1' : [20, ROOT.kGreen+2,  'type 1'],
                  'T2' : [21, ROOT.kBlue,     'type 2'],
                  'T3' : [22, ROOT.kRed,      'type 3']}
    ymax = 80.

# non irr angles
elif compareNum == 4: 
    nameComparison = 'nonIrr_angles'
    irr_label = 'non irradiated'
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

    plotAttrs = { 
                  '32' : [20, ROOT.kGreen+2,  '32^{o}'],
                  '52' : [21, ROOT.kBlue,     '52^{o}'],
                  '64' : [22, ROOT.kRed,      '64^{o}']}
    ymax = 100.





# 2E14 cell sizes
elif compareNum == 1:
    nameComparison = '2E14_cellSizes'
    irr_label = '2 #times 10^{14} 1 MeV n_{eq}/cm^{2}'  
    pars = [15,20, 25, 30]
    pars_to_scale = [20, 25, 30]
    angle_true = 49

    fnames = { 30 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_T-35C_angle52_cellSize.root',
               25 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_T-35C_angle52_cellSize.root',
               20 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_T-35C_angle52_cellSize.root',
               15 : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plots_timeResolution_2E14_15um_T2_TBJune22_TOFHIR2X.root'
              }
    labels = { 30 : 'HPK_2E14_LYSO200104_angle52_T-35C',
               25 : 'HPK_2E14_LYSO815_angle52_T-35C',
               20 : 'HPK_2E14_LYSO825_angle52_T-35C',
               15 : 'HPK_2E14_LYSO796_T-40C'
              }
    plotAttrs = { 30 : [23, ROOT.kOrange+1, '30 #mum'],
                  25 : [20, ROOT.kGreen+2,  '25 #mum'],
                  20 : [21, ROOT.kBlue,     '20 #mum'],
                  15 : [22, ROOT.kRed,      '15 #mum']
                 }
    ymin = 0.
    ymax = 160.
    xmin = 0.3
    xmax = 1.6


# types - irradiated 2E14
elif compareNum == 5:
    nameComparison = '2E14_types'
    irr_label = '2 #times 10^{14} 1 MeV n_{eq}/cm^{2}'
    
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
    ymax = 80.
    xmax = 1.6
    xmin = 0.4
    
# 2E14 rr angles
elif compareNum == 6:
    nameComparison = '2E14_angles'
    irr_label = '2 #times 10^{14} 1 MeV n_{eq}/cm^{2}'
    
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
    xmax = 1.6



# TYPE 1 - irradiated 1E14 - temperatures comparison
elif compareNum == 7:
    nameComparison  = '1E14_T1_temperatures'
    irr_label = '1 #times 10^{14} 1 MeV n_{eq}/cm^{2}'

    pars = ['-37', '-32', '-27', '-22']
    fnames = { '-37' : '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E14_LYSO819_temperatures.root',
               '-32' : '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E14_LYSO819_temperatures.root',
               '-27' : '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E14_LYSO819_temperatures.root',
               '-22' : '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E14_LYSO819_temperatures.root'
              }
    labels = { '-37' : 'HPK_1E14_LYSO819_angle52_T-37C',
               '-32' : 'HPK_1E14_LYSO819_angle52_T-32C',
               '-27' : 'HPK_1E14_LYSO819_angle52_T-27C',
               '-22' : 'HPK_1E14_LYSO819_angle52_T-22C'
              }
    plotAttrs = { 
                  '-37' : [20, 860,  '-37^{o}C'],
                  '-32' : [21, 870,     '-32^{o}C'],
                  '-27' : [22, 800,      '-27^{o}C'],
                  '-22' : [23,   2,      '-22^{o}C']
                 }
    ymax = 120.


# TYPE 1 - irradiated 1E13 - temperatures comparison
elif compareNum == 8:
    nameComparison = '1E13_T1_temperatures'
    pars = ['-32','-19','0','12']

    irr_label = '1 #times 10^{13} 1 MeV n_{eq}/cm^{2}'
    fnames = {
        '-32' : '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E13_LYSO829_temperatures.root',
        '-19' : '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E13_LYSO829_temperatures.root',
        '0'   : '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E13_LYSO829_temperatures.root',
        '12'  : '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E13_LYSO829_temperatures.root',
              }
    labels = {
        '-32' : 'HPK_1E13_LYSO829_angle52_T-32C',
        '-19' : 'HPK_1E13_LYSO829_angle52_T-19C',
        '0'   : 'HPK_1E13_LYSO829_angle52_T0C',
        '12'  : 'HPK_1E13_LYSO829_angle52_T12C',
              }
    plotAttrs = { 
        '-32' : [20,  860, '-32^{o}C'],
        '-19' : [21,  870, '-19^{o}C'],
        '0'   : [22,  800, '0^{o}C'],
        '12'  : [23,   2,  '12^{o}C'],
                 }
    ymax = 120.




    
    
enScale = {}

for it,par in enumerate(pars_to_scale):
    if not isinstance(angle_true, list):
        ang_true = angle_true
        angle_target = angle_true + angle_offset
    else:
        ang_true = angle_true[it]
        angle_target = angle_true[it] + angle_offset
    enScale[par] = math.cos(math.radians(ang_true)) / math.cos(math.radians(angle_target))
    
    




g_data = {}
g_noise = {}
g_stoch = {}
g_dcr = {}
g_sr = {}

g_data_scaled = {}
g_noise_scaled = {}
g_stoch_scaled = {}
g_dcr_scaled = {}


g_data_final = {}
g_noise_final = {}
g_stoch_final = {}
g_dcr_final = {}

f = {}

for par in pars:
    try:
        f[par] = ROOT.TFile.Open(fnames[par])
        if not f[par]:
            raise FileNotFoundError(f"File not found: {fnames[par]}")
        g_data[par] = f[par].Get('g_data_vs_Vov_average_%s'%labels[par])
        if not g_data[par]:
            raise AttributeError(f"Graph not found in file {fnames[par]} with name g_data_vs_Vov_average")
    except (FileNotFoundError, AttributeError) as e:
        print(f"Error: {e}")

    if par in pars_to_scale:
        g_data_scaled[par] = ROOT.TGraphErrors()
        g_noise_scaled[par] = ROOT.TGraphErrors()
        g_stoch_scaled[par] = ROOT.TGraphErrors()

        g_data_scaled[par].SetName('g_data_scaled_vs_Vov_average_%s'%labels[par]) 
        g_noise_scaled[par].SetName('g_Noise_scaled_vs_Vov_average_%s'%labels[par]) 
        g_stoch_scaled[par].SetName('g_Stoch_scaled_vs_Vov_average_%s'%labels[par]) 

        if not 'nonIrr' in nameComparison:
            g_dcr_scaled[par] = ROOT.TGraphErrors()
            g_dcr_scaled[par].SetName('g_DCR_scaled_vs_Vov_average_%s'%labels[par]) 

        
        
# scale contributions to take into account angle offset in 2023 Sep TB 
for par in pars:
    print("\n ", par)
    if (par not in fnames.keys()): continue
    g_noise[par] = f[par].Get('g_Noise_vs_Vov_average_%s'%labels[par])
    if 'nonIrr' in nameComparison:
        g_stoch[par] = f[par].Get('g_StochMeas_vs_Vov_average_%s'%labels[par])
    else:
        g_stoch[par] = f[par].Get('g_Stoch_vs_Vov_average_%s'%labels[par])
        
    if not 'nonIrr' in nameComparison:
        g_dcr[par]   = f[par].Get('g_DCR_vs_Vov_average_%s'%labels[par])
    g_sr[par]   = f[par].Get('g_SR_vs_Vov_average_%s'%labels[par])

    for i in range(0, g_data[par].GetN()):
        vov = g_data[par].GetX()[i]
        s_meas = g_data[par].GetY()[i]
        sr = g_sr[par].GetY()[i]
        err_sr = g_sr[par].GetEY()[i]
        if par in pars_to_scale:
            s_noise,err_s_noise =  sigma_noise(sr*enScale[par], '2c',err_sr)
            s_stoch = g_stoch[par].GetY()[i]/math.pow(enScale[par], stochPow)
            err_s_stoch = g_stoch[par].GetEY()[i]/math.pow(enScale[par], stochPow)
            g_noise_scaled[par].SetPoint(i, vov, s_noise)  
            g_noise_scaled[par].SetPointError(i, 0, err_s_noise) 
            g_stoch_scaled[par].SetPoint(i, vov, s_stoch)  
            g_stoch_scaled[par].SetPointError(i, 0, err_s_stoch) 
            s_dcr = 0.
            err_s_dcr = 0.
            
            if not 'nonIrr' in nameComparison:
                s_dcr = g_dcr[par].Eval(vov)/enScale[par]
                err_s_dcr = g_dcr[par].GetErrorY(i)/enScale[par]
                g_dcr_scaled[par].SetPoint(i, vov, s_dcr)  
                g_dcr_scaled[par].SetPointError(i, 0, err_s_dcr) 

            s_tot = math.sqrt(s_noise*s_noise + s_stoch*s_stoch + s_dcr*s_dcr)
            #err_s_tot = 1/s_tot * math.sqrt(math.pow(s_noise*err_s_noise,2) + math.pow(s_stoch*err_s_stoch,2) + math.pow(s_dcr*err_s_dcr,2))
            err_s_tot = g_data[par].GetEY()[i]
            
            g_data_scaled[par].SetPoint(i, vov, s_tot) 
            g_data_scaled[par].SetPointError(i, 0, err_s_tot) 

            

            #print("tot meas : ", round(s_meas,1), " tot scal in quadr: ", round(s_tot,1), " ---- noise true : ", round(sigma_noise(sr,"2c",err_sr)[0],1), "  noise scaled: ", round(s_noise,1), "  stoch true ", round(g_stoch[par].Eval(vov),1), "  stoch scaled ", round(s_stoch,1), ' dcr true : ', round(g_dcr[par].Eval(vov),1), ' dcr scaled : ', round(s_dcr,1))

for par in pars:
    if par in pars_to_scale:
        g_data_final[par] = g_data_scaled[par]
        g_stoch_final[par] = g_stoch_scaled[par]
        g_noise_final[par] = g_noise_scaled[par]
        if not 'nonIrr' in nameComparison:
            g_dcr_final[par] = g_dcr_scaled[par]
    else:
        g_data_final[par] = g_data[par]
        g_stoch_final[par] = g_stoch[par]
        g_noise_final[par] = g_noise[par]
        if not 'nonIrr' in nameComparison:
            g_dcr_final[par] = g_dcr[par]


        
# plot        
for par in pars:
    c = ROOT.TCanvas('c_timeResolution_components_%s_%s_vs_Vov'%(par, nameComparison), 'c_timeResolution_components_%s_%s_vs_Vov'%(par, nameComparison), 600, 500)
    if compareNum == 1 and par == 15:
        hPad = ROOT.gPad.DrawFrame(0.9, ymin, 2.2, ymax)
    else:
        hPad = ROOT.gPad.DrawFrame(xmin, ymin, xmax, ymax)
        
    #if (nameComparison == '2E14'): hPad = ROOT.gPad.DrawFrame(0., 0., 2., 160.)
    #    if '2E14' in nameComparison:
        #hPad = ROOT.gPad.DrawFrame(g_data_scaled[par].GetX()[0] - 0.2, 0., g_data_scaled[par].GetX()[0] + 1.2, ymax)
    hPad.SetTitle(";V_{OV} [V];time resolution [ps]")
    hPad.Draw()
    ROOT.gPad.SetTicks(1)
    
    g_data_final[par].SetMarkerStyle(20)
    g_data_final[par].SetMarkerSize(1)
    g_data_final[par].SetMarkerColor(1)
    g_data_final[par].SetLineColor(1)
    g_data_final[par].SetLineWidth(2)
    g_data_final[par].Draw('plsame')
    g_noise_final[par].SetLineWidth(2)
    g_noise_final[par].SetLineColor(ROOT.kBlue)
    g_noise_final[par].SetFillColor(ROOT.kBlue)
    g_noise_final[par].SetFillColorAlpha(ROOT.kBlue,0.5)
    g_noise_final[par].SetFillStyle(3004)
    g_noise_final[par].Draw('E3lsame')
    g_stoch_final[par].SetLineWidth(2)
    g_stoch_final[par].SetLineColor(ROOT.kGreen+2)
    g_stoch_final[par].SetFillColor(ROOT.kGreen+2)
    g_stoch_final[par].SetFillStyle(3001)
    g_stoch_final[par].SetFillColorAlpha(ROOT.kGreen+2,0.5)
    g_stoch_final[par].Draw('E3lsame')
    if not 'nonIrr' in nameComparison:
        g_dcr_final[par].SetLineWidth(2)
        g_dcr_final[par].SetLineColor(ROOT.kOrange+2)
        g_dcr_final[par].SetFillColor(ROOT.kOrange+2)
        g_dcr_final[par].SetFillStyle(3005)
        g_dcr_final[par].Draw('E3lsame')

    leg = ROOT.TLegend(0.70, 0.62, 0.89, 0.89)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.050)
    leg.AddEntry(g_data_final[par], 'data', 'PL')
    leg.AddEntry(g_noise_final[par], 'electronics', 'FL')
    leg.AddEntry(g_stoch_final[par], 'photo-stat.', 'FL')    
    if not 'nonIrr' in nameComparison:
        leg.AddEntry(g_dcr_final[par], 'DCR', 'FL')    
    leg.Draw()
    
    tl = ROOT.TLatex()
    tl.SetNDC()
    tl.SetTextFont(42)
    tl.SetTextSize(0.050)
    if compareNum == 1 or compareNum ==2:
        tl.DrawLatex(0.20,0.86,'HPK, %s'%plotAttrs[par][2])
        print(plotAttrs[par][2])
    else:
        tl.DrawLatex(0.20,0.86,'HPK, 25 #mum')

    tl3 = ROOT.TLatex()
    tl3.SetNDC()
    tl3.SetTextFont(42)
    tl3.SetTextSize(0.050)
    tl3.DrawLatex(0.20,0.80,'{}'.format(irr_label))

    #cms_logo = draw_logo()
    #cms_logo.Draw()

    c.SaveAs(outdir+'%s.png'%c.GetName())
    c.SaveAs(outdir+'%s.pdf'%c.GetName())

    
