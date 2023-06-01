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
from thickeningScenario import *

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

#plotsdir = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots'
#plotsdir = '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots'
scenariosList = []


# --------CAMBIA QUI---------------------------------------
compareNum = 2

if compareNum == 1:
    outSuffix = 'HPK_irr_BTLlike_mid'
    scenariosList.append(standard_BTLlike)
    #scenariosList.append(mixed)   ## mixed does not exist for btl like
    scenariosList.append(allT1_BTLlike)

elif compareNum == 2:
    outSuffix = 'HPK_irr_EoL_emulation'
    scenariosList.append(standard_EoL)
    scenariosList.append(mixed_EoL)
    scenariosList.append(allT1_EoL)



# ---------------------------------------------------------



Vovs_given = True
Vovs_list = [0.6,0.8,0.9,1.1]

for obj in scenariosList:
    for it,sipm in enumerate(obj.sipmTypes):
        obj.sipmTypes[it] = sipm + obj.extraName[it]

    print '', obj.sipmTypes,  '  ', obj.fname , ' ', obj.angles




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

    leg = ROOT.TLegend(0.77,0.72,0.90,0.90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    
    for it, obj in enumerate(scenariosList):
        lbl = obj.label
        if ov not in VovsUnion[lbl]: continue

        g_t_vs_RU[lbl][ov].SetLineColor(obj.color)
        g_t_vs_RU[lbl][ov].SetFillColor(obj.color)
        g_t_vs_RU[lbl][ov].SetFillColorAlpha(obj.color, 0.5)
        g_t_vs_RU[lbl][ov].SetFillStyle(3001)
        g_t_vs_RU[lbl][ov].Draw('E3lsame')
        
        leg.AddEntry(g_t_vs_RU[lbl][ov], '%s'%lbl, 'l')
    leg.Draw('same')

    latex = ROOT.TLatex(0.2,0.87,'Vov%.2f'%ov)
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextFont(42)
    latex.Draw('same')


    logo = ROOT.TLatex()
    logo.SetNDC()
    logo.SetTextSize(0.045) 
    logo.SetTextFont(62)
    logo.DrawText(0.16,0.95,'CMS') 
    logo.SetTextFont(52)
    logo.DrawText(0.22, 0.95, '  Preliminary')

        
    c.SaveAs(outdir+'/'+c.GetName()+'.png')
