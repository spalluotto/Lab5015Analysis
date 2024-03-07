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
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning



# ---- EDIT ---- 
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'
angle_offset = 3
# -------------

#---- init ---
parser = argparse.ArgumentParser()  
parser.add_argument("-n","--comparisonNumber", required = True, type=str, help="comparison number")    
args = parser.parse_args()   

compareNum = int(args.comparisonNumber)


fnames = {}
gnames = {}
labels = {}


if compareNum == 1:
    nameComparison = '2E14_cellSizes'
    labelComparison = '2 #times 10^{14} 1 MeV n_{eq}/cm^{2}'  
    pars = [15, 20, 25, 30]
    pars_to_scale = [15, 25, 30]
    angle_true = 49

    fnames = { 30 : '/eos/user/m/malberti/www/MTD/TOFHIR2C/MTDTB_CERN_Sep23/timeResolution_2E14_20um_25um_30um_T2/plots_timeResolution_2E14_20um_25um_30um_T2_TBSep23_TOFHIR2C.root',
               25 : '/eos/user/m/malberti/www/MTD/TOFHIR2C/MTDTB_CERN_Sep23/timeResolution_2E14_20um_25um_30um_T2/plots_timeResolution_2E14_20um_25um_30um_T2_TBSep23_TOFHIR2C.root',
               20 : '/eos/user/m/malberti/www/MTD/TOFHIR2C/MTDTB_CERN_Sep23/timeResolution_2E14_20um_25um_30um_T2/plots_timeResolution_2E14_20um_25um_30um_T2_TBSep23_TOFHIR2C.root',
               15 : '/eos/user/m/malberti/www/MTD/TOFHIR2X/MTDTB_CERN_Jun22/timeResolution_2E14_15um_T2/plots_timeResolution_2E14_15um_T2_TBJune22_TOFHIR2X.root'}

    gnames = { 30 : 'g_data_vs_Vov_average_HPK_2E14_LYSO200104_T-35C_TOFHIR2C',
               25 : 'g_data_vs_Vov_average_HPK_2E14_LYSO815_T-35C_TOFHIR2C',
               20 : 'g_data_vs_Vov_average_HPK_2E14_LYSO825_T-35C_TOFHIR2C',
               15 : 'g_data_vs_Vov_average_HPK_2E14_LYSO796_T-40C'  # less annealing for this module
              }

    labels = { 30 : 'HPK_2E14_LYSO200104_T-35C_TOFHIR2C',
               25 : 'HPK_2E14_LYSO815_T-35C_TOFHIR2C',
               20 : 'HPK_2E14_LYSO825_T-35C_TOFHIR2C',
               15 : 'HPK_2E14_LYSO796_T-40C'
              }
    plotAttrs = { 30 : [23, ROOT.kOrange+1, '30 #mum'],
                  25 : [20, ROOT.kGreen+2,  '25 #mum'],
                  20 : [21, ROOT.kBlue,     '20 #mum'],
                  15 : [22, ROOT.kRed,      '15 #mum']}

    ymax = 160.

    
elif compareNum == 2:
    nameComparison = 'nonIrr_cellSizes'
    labelComparison = 'non irradiated'
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



elif compareNum == 3:
    nameComparison = 'nonIrr_types'
    labelComparison = 'non irradiated'
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





# ---- TO BE FIXED !!!! devo sistemare plot tres irr in modo da fare si che lo stocastico sia quello atteso e non quello misurato +  controllare pulse shape etc
elif compareNum == 4:
    nameComparison = '2E14_types'
    labelComparison = '2 #times 10^{14} 1 MeV n_{eq}/cm^{2}'
    pars = ['T1', 'T2', 'T3']
    pars_to_scale = pars
    angle_true = 61

    fnames = { 'T1' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_T-35C_angle64_types.root',
               'T2' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_T-35C_angle64_types.root',
               'T3' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_T-35C_angle64_types.root'
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


    

angle_target = angle_true + angle_offset
enScale = math.cos(math.radians(angle_true)) / math.cos(math.radians(angle_target))




gData = {}
gNoise = {}
gStoch = {}
gDCR = {}
gSR = {}

gData_scaled = {}
gNoise_scaled = {}
gStoch_scaled = {}
gDCR_scaled = {}

f = {}

for par in pars:
    try:
        f[par] = ROOT.TFile.Open(fnames[par])
        if not f[par]:
            raise FileNotFoundError(f"File not found: {fnames[par]}")
        gData[par] = f[par].Get('g_data_vs_Vov_average_%s'%labels[par])
        if not gData[par]:
            raise AttributeError(f"Graph not found in file {fnames[par]} with name {graph_name}")
    except (FileNotFoundError, AttributeError) as e:
        print(f"Error: {e}")

    gData_scaled[par] = ROOT.TGraphErrors()
    gNoise_scaled[par] = ROOT.TGraphErrors()
    gStoch_scaled[par] = ROOT.TGraphErrors()

    gData_scaled[par].SetName('g_data_scaled_vs_Vov_average_%s'%labels[par]) 
    gNoise_scaled[par].SetName('g_Noise_scaled_vs_Vov_average_%s'%labels[par]) 
    gStoch_scaled[par].SetName('g_Stoch_scaled_vs_Vov_average_%s'%labels[par]) 

    if not 'nonIrr' in nameComparison:
        gDCR_scaled[par] = ROOT.TGraphErrors()
        gDCR_scaled[par].SetName('g_DCR_scaled_vs_Vov_average_%s'%labels[par]) 

        
        
# scale contributions to take into account angle offset in 2023 Sep TB 
for par in pars:
    if (par not in fnames.keys()): continue
    gNoise[par] = f[par].Get('g_Noise_vs_Vov_average_%s'%labels[par])
    gStoch[par] = f[par].Get('g_Stoch_vs_Vov_average_%s'%labels[par])
    gDCR[par]   = f[par].Get('g_DCR_vs_Vov_average_%s'%labels[par])
    gSR[par]   = f[par].Get('g_SR_vs_Vov_average_%s'%labels[par])
    # if 15 um from June22 TB non need to scale for angle offset.
    if ('TBJun22' in fnames[par] ): enScale = 1.
    for i in range(0, gData[par].GetN()):
        vov = gData[par].GetX()[i]
        sr = gSR[par].Eval(vov)
        s_noise =  sigma_noise(sr*enScale, '2c')
        s_stoch = gStoch[par].Eval(vov)/math.sqrt(enScale)
        s_dcr = 0.
        s_tot = math.sqrt(s_noise*s_noise + s_stoch*s_stoch + s_dcr*s_dcr)
        gData_scaled[par].SetPoint(i, vov, s_tot) 
        gData_scaled[par].SetPointError(i, 0, gData[par].GetErrorY(i)/enScale) 
        gNoise_scaled[par].SetPoint(i, vov, s_noise)  
        gNoise_scaled[par].SetPointError(i, 0, gNoise[par].GetErrorY(i)/enScale) 
        gStoch_scaled[par].SetPoint(i, vov, s_stoch)  
        gStoch_scaled[par].SetPointError(i, 0, gStoch[par].GetErrorY(i)/math.sqrt(enScale)) 

        if not 'nonIrr' in nameComparison:
            s_dcr = gDCR[par].Eval(vov)/enScale
            gDCR_scaled[par].SetPoint(i, vov, s_dcr)  
            gDCR_scaled[par].SetPointError(i, 0, gDCR[par].GetErrorY(i)/enScale) 


# plot        
for par in pars:
    c = ROOT.TCanvas('c_timeResolution_components_%s_%s_vs_Vov'%(par, nameComparison), 'c_timeResolution_components_%s_%s_vs_Vov'%(par, nameComparison), 600, 500)
    hPad = ROOT.gPad.DrawFrame(0., 0., 4.0, ymax)
    #if (nameComparison == '2E14'): hPad = ROOT.gPad.DrawFrame(0., 0., 2., 160.)
    if '2E14' in nameComparison:
        hPad = ROOT.gPad.DrawFrame(gData_scaled[par].GetX()[0] - 0.2, 0., gData_scaled[par].GetX()[0] + 1.2, ymax)
    hPad.SetTitle(";V_{OV} [V];time resolution [ps]")
    hPad.Draw()
    ROOT.gPad.SetTicks(1)
    
    gData_scaled[par].SetMarkerStyle(20)
    gData_scaled[par].SetMarkerSize(1)
    gData_scaled[par].SetMarkerColor(1)
    gData_scaled[par].SetLineColor(1)
    gData_scaled[par].SetLineWidth(2)
    gData_scaled[par].Draw('plsame')
    gNoise_scaled[par].SetLineWidth(2)
    gNoise_scaled[par].SetLineColor(ROOT.kBlue)
    gNoise_scaled[par].SetFillColor(ROOT.kBlue)
    gNoise_scaled[par].SetFillColorAlpha(ROOT.kBlue,0.5)
    gNoise_scaled[par].SetFillStyle(3004)
    gNoise_scaled[par].Draw('E3lsame')
    gStoch_scaled[par].SetLineWidth(2)
    gStoch_scaled[par].SetLineColor(ROOT.kGreen+2)
    gStoch_scaled[par].SetFillColor(ROOT.kGreen+2)
    gStoch_scaled[par].SetFillStyle(3001)
    gStoch_scaled[par].SetFillColorAlpha(ROOT.kGreen+2,0.5)
    gStoch_scaled[par].Draw('E3lsame')
    if not 'nonIrr' in nameComparison:
        gDCR_scaled[par].SetLineWidth(2)
        gDCR_scaled[par].SetLineColor(ROOT.kOrange+2)
        gDCR_scaled[par].SetFillColor(ROOT.kOrange+2)
        gDCR_scaled[par].SetFillStyle(3001)
        gDCR_scaled[par].SetFillColorAlpha(ROOT.kOrange+2,0.5)
        gDCR_scaled[par].Draw('E3lsame')

    leg = ROOT.TLegend(0.70, 0.60, 0.89, 0.89)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.050)
    leg.AddEntry(gData_scaled[par], 'data', 'PL')
    leg.AddEntry(gNoise_scaled[par], 'noise', 'FL')
    leg.AddEntry(gStoch_scaled[par], 'stochastic', 'FL')    
    if not 'nonIrr' in nameComparison:
        leg.AddEntry(gDCR_scaled[par], 'DCR', 'FL')    
    leg.Draw()
    
    tl = ROOT.TLatex()
    tl.SetNDC()
    tl.SetTextFont(42)
    tl.SetTextSize(0.050)
    tl.DrawLatex(0.20,0.86,'%s'%plotAttrs[par][2])

    tl3 = ROOT.TLatex()
    tl3.SetNDC()
    tl3.SetTextFont(42)
    tl3.SetTextSize(0.050)
    tl3.DrawLatex(0.20,0.80,'{}'.format(labelComparison))

    cms_logo = draw_logo()
    cms_logo.Draw()

    c.SaveAs(outdir+'%s.png'%c.GetName())
    c.SaveAs(outdir+'%s.pdf'%c.GetName())

    
