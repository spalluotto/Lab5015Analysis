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
ROOT.gStyle.SetPadRightMargin(0.05)
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning






# ---- EDIT ---- 
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'
angle_offset = 3
pars_to_scale = []
# -------------

stochPow = 0.76

srScale = 1.20 # scaling SR from TOFHIR2X to 2C
pars_srScale = []
index_out_of_bounds = False
ov_min = 0.
ov_max = 2.
power_min = 0.
power_max = 120.
ymin = 20.

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
    pars = [15,20, 25, 30]
    pars_to_scale = [20, 25, 30]
    angle_true = 49
    label_on_top = 'HPK'
    
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
    ymax = 160.
    ov_min = 0.2
    ov_max = 2.4

    
# types
elif compareNum == 2:
    nameComparison = 'HPK_2E14_types'
    pars = ['T1', 'T2', 'T3']
    pars_to_scale = pars
    angle_true = 61
    label_on_top = 'HPK, 25 #mum'


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
    ov_min = 0.2
    ov_max = 1.4
    

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

    label_on_top = 'HPK, 25 #mum'
    plotAttrs = { 
                  '32' : [20, ROOT.kGreen+2,  '32^{o}'],
                  '52' : [21, ROOT.kBlue,     '52^{o}'],
                  '64' : [22, ROOT.kRed,      '64^{o}']}
    ymax = 120.
    ov_min = 0.2
    ov_max = 1.4
    power_max = 60.



# TYPE 1 - irradiated 2E14 - temperatures comparison
elif compareNum == 4:
    nameComparison = 'HPK_2E14_T1_temperatures'
    pars = ['-30', '-35', '-40']
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
    label_on_top = 'HPK, 25 #mum'

    plotAttrs = { 
                  '-40' : [20, 860,  '-40^{o}C'],
                  '-35' : [21, 800,     '-35^{o}C'],
                  '-30' : [22, 2,      '-30^{o}C']
                 }
    ymax = 100.
    ov_min = 0.2
    ov_max = 1.4
    power_max = 60.



# TYPE 1 - irradiated 1E14 - temperatures comparison
elif compareNum == 5:
    nameComparison = 'HPK_1E14_T1_temperatures'
    pars = [ '-22', '-27','-32','-37']
    
    irr_label = '1 #times 10^{14} 1 MeV n_{eq}/cm^{2}'
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
    label_on_top = 'HPK, 25 #mum'

    plotAttrs = { 
        '-37' : [20, 860,  '-37^{o}C'],
        '-32' : [21, 870,     '-32^{o}C'],
        '-27' : [22, 800,      '-27^{o}C'],
        '-22' : [23,   2,      '-22^{o}C']
                 }
    ymax = 100.
    ov_min = 0.2
    ov_max = 1.8
    

# TYPE 1 - irradiated 1E13 - temperatures comparison
elif compareNum == 6:
    nameComparison = 'HPK_1E13_T1_temperatures'
    pars = ['12', '0','-19','-32']
    
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
    label_on_top = 'HPK, 25 #mum'

    plotAttrs = { 
        '-32' : [20,  860, '-32^{o}C'],
        '-19' : [21,  870, '-19^{o}C'],
        '0'   : [22,  800, '0^{o}C'],
        '12'  : [23,   2,  '12^{o}C'],
                 }
    ymax = 100.
    ov_min = 0.4
    ov_max = 2.4
    power_max = 40.



# ------- T1 --- different fluences at the BTL equivalent temperature
elif compareNum == 7:
    nameComparison = 'HPK_irr_T1_temperatures_BTLeq'
    pars = ['-35', '-32', '-19']
    pars_to_scale = ['-35', '-32']

    angle_true = 49
    irr_label = 'BTL equivalent'
    fnames = {
        '-35' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_temperatures.root',
        '-32' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_1E14_LYSO819_temperatures.root',
        '-19' : '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E13_LYSO829_temperatures.root',
    }
    labels = {
        '-35' : 'HPK_2E14_LYSO100056_angle52_T-35C',
        '-32' : 'HPK_1E14_LYSO819_angle52_T-32C',
        '-19' : 'HPK_1E13_LYSO829_angle52_T-19C',
              }
    label_on_top = 'HPK, 25 #mum'

    plotAttrs = {
        '-35' : [20, 3,     '-35^{o}C'],
        '-32' : [21, 4,     '-32^{o}C'],
        '-19' : [22,   2,     '-19^{o}C'],
                 }
    ov_min = 0.2
    ymax = 100.
    power_max = 60.
    
    
# energy scaling for angle offset
enScale = {}
for it,par in enumerate(pars_to_scale):
    if not isinstance(angle_true, list):
        ang_true = angle_true
        angle_target = angle_true + angle_offset
    else:
        ang_true = angle_true[it]
        angle_target = angle_true[it] + angle_offset
    enScale[par] = math.cos(math.radians(ang_true)) / math.cos(math.radians(angle_target))


# define objects
g = {}
g_vs_power = {}

g_scaled = {}
g_scaled_vs_power = {}

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
        g_vs_power[par] = f[par].Get('g_data_vs_staticPower_average_%s'%labels[par])
        if not g_vs_power[par]:
            print('g_data_vs_staticPower_average_',labels[par],'  not found in  ', fnames[par])
            raise AttributeError("Graph not found in file")
    except (FileNotFoundError, AttributeError) as e:
        print(f"Error: {e}")
    g_scaled[par] = ROOT.TGraphErrors()
    g_scaled[par].SetName('g_data_scaled_vs_Vov_average_%s'%labels[par])

    g_scaled_vs_power[par] = ROOT.TGraphErrors()
    g_scaled_vs_power[par].SetName('g_data_scaled_vs_staticPower_average_%s'%labels[par])

# scale 2X --> 2C
if pars_srScale:
    for par in pars_srScale:
        g_Noise[par] = f[par].Get('g_Noise_vs_Vov_average_%s'%labels[par])
        g_Stoch[par] = f[par].Get('g_Stoch_vs_Vov_average_%s'%labels[par])
        g_DCR[par]   = f[par].Get('g_DCR_vs_Vov_average_%s'%labels[par])
        g_SR[par]    = f[par].Get('g_SR_vs_Vov_average_%s'%labels[par])
        
        for i in range(0, g[par].GetN()):
            vov = g[par].GetX()[i]
            if round(vov,2) != round(g_SR[par].GetX()[i],2):
                print("Vov from SR vs Vov is different in index wrt data vs Vov")
                sys.exit()
            sr = g_SR[par].GetY()[i]
            err_sr = g_SR[par].GetEY()[i]

            #sr = g_SR[par].Eval(vov)  # AGGIUNGI ERRORE SU SR
            s_noise_scaled = sigma_noise(sr*srScale, '2c', err_sr)
            s_stoch = g_Stoch[par].Eval(vov)
            s_dcr = g_DCR[par].Eval(vov)
            s_tot = math.sqrt(s_noise_scaled*s_noise_scaled + s_stoch*s_stoch + s_dcr*s_dcr)
            g_scaled[par].SetPoint(i, vov, s_tot)
            g_scaled[par].SetPointError(i, 0, g[par].GetErrorY(i))

            g_scaled_vs_power[par].SetPoint(i, g_vs_power[par].GetX()[i], s_tot)
            g_scaled_vs_power[par].SetPointError(i, 0 , g_scaled_vs_power[par].GetErrorY(i))

# scale others (2C) to take into account angle offset in 2023 Sep TB 
for par in pars_to_scale:
    print("\n ", par)
    g_Noise[par] = f[par].Get('g_Noise_vs_Vov_average_%s'%labels[par])
    g_Stoch[par] = f[par].Get('g_Stoch_vs_Vov_average_%s'%labels[par])
    g_SR[par]   = f[par].Get('g_SR_vs_Vov_average_%s'%labels[par])
    g_DCR[par]   = f[par].Get('g_DCR_vs_Vov_average_%s'%labels[par])

    for i in range(0, g[par].GetN()):
        vov = g[par].GetX()[i]
        if round(vov,2) != round(g_SR[par].GetX()[i],2):
            print("Vov from SR vs Vov is different in index wrt data vs Vov")
            sys.exit()
        sr = g_SR[par].GetY()[i]
        err_sr = g_SR[par].GetEY()[i]
        s_noise,err_s_noise =  sigma_noise(sr*enScale[par], '2c', err_sr)  # AGGIUNGI ERRORE SU SR

        if round(vov,2) != round(g_Stoch[par].GetX()[i],2):
            print("Vov from Stoch vs Vov is different in index wrt data vs Vov")
            sys.exit()

        s_stoch = g_Stoch[par].Eval(vov)/math.pow(enScale[par], stochPow)
        err_s_stoch = g_Stoch[par].GetEY()[i]/math.pow(enScale[par],stochPow)
        
        s_dcr = g_DCR[par].Eval(vov)/enScale[par]
        err_s_dcr = g_DCR[par].GetEY()[i]/enScale[par]

        s_tot = math.sqrt(s_noise*s_noise + s_stoch*s_stoch + s_dcr*s_dcr)
        err_s_tot = 1./s_tot * math.sqrt( pow( err_s_stoch*s_stoch,2) + pow(s_noise*err_s_noise,2) + pow(s_dcr*err_s_dcr,2))
        
        print("tot : ", s_tot, " ---- noise true : ", sigma_noise(sr,"2c",err_sr), "  noise scaled: ", s_noise, "  stoch true ", g_Stoch[par].Eval(vov), "  stoch scaled ", s_stoch, ' dcr true : ', g_DCR[par].Eval(vov), ' dcr scaled : ', s_dcr)

        g_scaled[par].SetPoint(g_scaled[par].GetN(), vov, s_tot) # correct for angle offset
        g_scaled[par].SetPointError(g_scaled[par].GetN()-1, 0, err_s_tot)
        #g_scaled[par].SetPointError(i, 0, g[par].GetErrorY(i)/enScale[par]) # correct for angle offset                            

        try:
            g_scaled_vs_power[par].SetPoint(i, g_vs_power[par].GetX()[i], s_tot)
            g_scaled_vs_power[par].SetPointError(i, 0 , err_s_tot)
        except IndexError:
            index_out_of_bounds = True
            print("Index out of bounds")
            
            
        
# plot
leg = ROOT.TLegend(0.70, 0.60, 0.89, 0.89)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045) 

c = ROOT.TCanvas('c_timeResolution_%s_vs_Vov'%nameComparison,'c_timeResolution_%s_vs_Vov'%nameComparison, 600, 500)
hPad = ROOT.gPad.DrawFrame(ov_min,ymin,ov_max,ymax)
hPad.SetTitle(";V_{OV} [V];time resolution [ps]")
hPad.Draw()
ROOT.gPad.SetTicks(1)
for par in pars:
    if par in pars_to_scale:
        g_scaled[par].SetMarkerSize(1)
        if (plotAttrs[par][0] == 22 or plotAttrs[par][0] == 23): g_scaled[par].SetMarkerSize(1.15)
        g_scaled[par].SetMarkerStyle(plotAttrs[par][0])
        g_scaled[par].SetMarkerColor(plotAttrs[par][1])
        g_scaled[par].SetLineColor(plotAttrs[par][1])
        leg.AddEntry(g_scaled[par], '%s'%plotAttrs[par][2],'PL')
        g_scaled[par].Draw('plsame')
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
#tl2.DrawLatex(0.20,0.86,'%s'%nameComparison.split('_')[0])
tl2.DrawLatex(0.20,0.86,'%s'%label_on_top)


tl = ROOT.TLatex()
tl.SetNDC()
tl.SetTextFont(42)
tl.SetTextSize(0.045)
tl.DrawLatex(0.20,0.80, irr_label)

cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'%s.png'%c.GetName())
c.SaveAs(outdir+'%s.pdf'%c.GetName())


# outfile   = ROOT.TFile.Open(outdir+'/%s.root'%c.GetName(),'recreate')
# for par in pars:
#     outfile.cd()
#     g_scaled[par].Write(g_scaled[par].GetName())


if not index_out_of_bounds:
    c_ = ROOT.TCanvas('c_timeResolution_%s_vs_staticPower'%nameComparison,'c_timeResolution_%s_vs_staticPower'%nameComparison, 600, 500)
    c_.cd()
    hPad = ROOT.gPad.DrawFrame(power_min,ymin,power_max,ymax)
    hPad.SetTitle(";static power [mW];time resolution [ps]")
    hPad.Draw()
    ROOT.gPad.SetTicks(1)
    for par in pars:
        if par in pars_to_scale:
            g_scaled_vs_power[par].SetMarkerSize(1)
            if (plotAttrs[par][0] == 22 or plotAttrs[par][0] == 23): g_scaled_vs_power[par].SetMarkerSize(1.15)
            g_scaled_vs_power[par].SetMarkerStyle(plotAttrs[par][0])
            g_scaled_vs_power[par].SetMarkerColor(plotAttrs[par][1])
            g_scaled_vs_power[par].SetLineColor(plotAttrs[par][1])
            g_scaled_vs_power[par].Draw('plsame')
        else:
            g_vs_power[par].SetMarkerStyle(plotAttrs[par][0])
            g_vs_power[par].SetMarkerColor(plotAttrs[par][1])
            g_vs_power[par].SetMarkerSize(1.15)
            g_vs_power[par].SetLineColor(plotAttrs[par][1])
            g_vs_power[par].SetLineWidth(1)
            g_vs_power[par].Draw('plsame')
            
    leg.Draw()
    #tl2.DrawLatex(0.20,0.86,'%s'%nameComparison.split('_')[0])
    tl2.DrawLatex(0.20,0.86,'%s'%label_on_top)
    tl.DrawLatex(0.20,0.80, irr_label)
    
    cms_logo = draw_logo()
    cms_logo.Draw()
    
    c_.SaveAs(outdir+'%s.png'%c_.GetName())
    c_.SaveAs(outdir+'%s.pdf'%c_.GetName())
