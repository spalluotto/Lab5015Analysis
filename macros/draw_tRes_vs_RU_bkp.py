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
import tdrstyle
from SiPM import *
from slewRate import *
from moduleDict import *
from thickneningScenario import *

ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.SetBatch(False)
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0111)


plotsdir = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots'

Vovs_given = True
Vovs_list = [0.6,0.8,0.9,1.1]




class scenario:
    def __init__(self):
        scenario.sipmTypes = ['','','']
        scenario.fname = ''
        scenario.extraLabel = ['','','']
        scenario.extraName = ['','','']
        scenario.angles = [0,0,0]
        scenario.label = ''
        # scenario.posCor = [7,10,15]
        scenario.posCor = [0,0,0]

#--------CAMBIA QUI------------------------------------------------------------------


#--- T1 T2 T3
standard = scenario()
standard.sipmTypes = ['HPK_1E14_LYSO819','HPK_2E14_LYSO815','HPK_1E14_LYSO817']
standard.fname = '%s/compareTimeResolution_vs_Vov_EoL_T1_T2_T3.root'%plotsdir
standard.extraName  = ['_angle32_T-22C', '_angle52_T-35C', '_angle64_T-22C']
standard.angles = [32, 52, 64]
standard.label = 'T1 T2 T3'
standard.posCor = [7,10,10]


#--- T1 T2 T2
mixed = scenario()
mixed.sipmTypes = ['HPK_1E14_LYSO819','HPK_2E14_LYSO815','HPK_2E14_LYSO815']
mixed.fname = '%s/compareTimeResolution_vs_Vov_EoL_T1_T2_T2.root'%plotsdir
mixed.extraName  = ['_angle32_T-22C', '_angle52_T-35C', '_angle64_T-35C']
mixed.angles = [32, 52, 64]
mixed.label = 'T1 T2 T2'
mixed.posCor = [7,10,15]

#--- T1 T1 T1
allT1 = scenario()
allT1.sipmTypes = ['HPK_1E14_LYSO819','HPK_1E14_LYSO819','HPK_1E14_LYSO819']
allT1.fname = '%s/compareTimeResolution_vs_Vov_EoL_T1_T1_T1.root'%plotsdir
allT1.extraName  = ['_angle32_T-22C', '_angle52_T-22C', '_angle64_T-22C']
allT1.angles = [32, 52, 64]
allT1.label = 'T1 T1 T1'
allT1.posCor = [7,10,15]



outSuffix = 'HPK_irr_EoL_emulation'



scenariosList = []
scenariosList.append(standard)
scenariosList.append(mixed)
scenariosList.append(allT1)

for obj in scenariosList:
    for it,sipm in enumerate(obj.sipmTypes):
        obj.sipmTypes[it] = sipm + obj.extraName[it]

    print '', obj.sipmTypes,  '  ', obj.fname , ' ', obj.angles



color_map = [850,880,800,840,910]



#--------------------------------------------------------------------------------------

# ----- output --------
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_May23/study_diff_angles/%s/'%outSuffix
if (os.path.exists(outdir)==False):
    os.mkdir(outdir)

#---------



# --- retrieve bars and ovs from compareTRes plots 
Vovs_tot = []
VovsUnion = {}
g_t = {}
Vovs = {}

for ii, obj in enumerate(scenariosList):
    lbl = obj.label

    VovsUnion[lbl] = []
    Vovs[lbl] = {}

    f = ROOT.TFile.Open(obj.fname)

    print 'scenario ', lbl

    g_t[lbl] = {}


    for j,sipm in enumerate(obj.sipmTypes):
        print 'sipm: ', sipm
        if '816' in sipm:
            f2 = ROOT.TFile.Open(scaling_file)
            g_t[lbl][sipm] = f2.Get('g_%s'%sipm)
        else:
            g_t[lbl][sipm] = f.Get('g_%s'%sipm)

        Vovs[lbl][sipm] = []
        if not Vovs_given:
            for ipoint in range(g_t[lbl][sipm].GetN()):
                Vovs[lbl][sipm].append(g_t[lbl][sipm].GetX()[ipoint])
        else:
            Vovs[lbl][sipm] = Vovs_list
        if j == 0:  
            VovsUnion[lbl] = Vovs[lbl][sipm]
        else:
            VovsUnion[lbl] = union(VovsUnion[lbl], Vovs[lbl][sipm]) 

    print 'ovs: ', VovsUnion[lbl] , '  --> ', lbl

    if ii == 0:
        Vovs_tot = VovsUnion[lbl]
    else:
        Vovs_tot = union(Vovs_tot, VovsUnion[lbl])

print 'ovs tot: ', Vovs_tot


#----- time resolution  --
g_t_vs_RU = {}
line_t_vs_RU = {}
erY = {}

for obj in scenariosList:
    lbl = obj.label
    g_t_vs_RU[lbl] = {}
    line_t_vs_RU[lbl] = {}
    for ov in VovsUnion[lbl]:
        print '\n\nov: ', ov
        g_t_vs_RU[lbl][ov] = ROOT.TGraphErrors()
        line_t_vs_RU[lbl][ov] = {}

        for it, sipm in enumerate(obj.sipmTypes):
            if ov not in Vovs[lbl][sipm]: continue

            line_t_vs_RU[lbl][ov][sipm] = ROOT.TLine(it*2, g_t[lbl][sipm].Eval(ov), it*2+2, g_t[lbl][sipm].Eval(ov))
            
            erY = 0

            if not Vovs_given:
                for ipoint in range(g_t[lbl][sipm].GetN()):
                    if ov == g_t[lbl][sipm].GetX()[ipoint]:
                        erY = g_t[lbl][sipm].GetErrorY(ipoint)                
            else:
                erY = g_t[lbl][sipm].Eval(ov)/100*6


            for iRU in range(2):
                tmp = math.sqrt( math.pow(g_t[lbl][sipm].Eval(ov),2) - math.pow(obj.posCor[it],2) )
                if iRU == 0:
                    ru = it*2
                else:
                    ru = it*2+1.99


                g_t_vs_RU[lbl][ov].SetPoint(g_t_vs_RU[lbl][ov].GetN(), ru, tmp)
                g_t_vs_RU[lbl][ov].SetPointError(g_t_vs_RU[lbl][ov].GetN()-1, 2, erY)

            print 'obj: ', lbl, '  sipm  ', sipm, '    ru ', ru, '   tRes    ', tmp 

                #  0       1       2
                #  0 1.99  2 3.99  4 5.99






# ---- draw -----
for ov in Vovs_tot:
    c = ROOT.TCanvas('c_timeResolution_vs_RU_Vov%.2f'%ov, '', 900, 700)
    c.cd()
    c.SetGridx()
    c.SetGridy()
    hPad = ROOT.TH2F('','',100,-1,7,100,0,80)
    hPad.GetXaxis().SetTitle('RU')
    hPad.GetYaxis().SetTitle('#sigma_{t} [ps]')
    hPad.Draw()

    leg = ROOT.TLegend(0.62,0.72,0.90,0.90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    
    for it, obj in enumerate(scenariosList):
        lbl = obj.label
        if ov not in VovsUnion[lbl]: continue

        g_t_vs_RU[lbl][ov].SetLineColor(it+1)
        g_t_vs_RU[lbl][ov].SetFillColor(it+1)
        g_t_vs_RU[lbl][ov].SetFillColorAlpha(it+1, 0.5)
        g_t_vs_RU[lbl][ov].SetFillStyle(3001)
        g_t_vs_RU[lbl][ov].Draw('E3lsame')
        
        leg.AddEntry(g_t_vs_RU[lbl][ov], '%s'%lbl, 'l')
    leg.Draw('same')

    latex = ROOT.TLatex(0.15,0.83,'Vov%.2f'%ov)
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextFont(42)
    latex.Draw('same')
        
    c.SaveAs(outdir+'/'+c.GetName()+'.png')
