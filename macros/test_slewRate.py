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

from slewRate import *
from SiPM import *
from moduleDict import *

parser = argparse.ArgumentParser()  
parser.add_argument("-n","--comparisonNumber", required = True, type=str, help="comparison number")    
args = parser.parse_args()   


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

def latex_vov(overv):
    latex_tmp = ROOT.TLatex(0.19,0.88,'Vov%.2f'%overv)
    latex_tmp.SetNDC()
    latex_tmp.SetTextSize(0.035)
    latex_tmp.SetTextFont(42)
    return latex_tmp

def latex_sipm(sip_):
    latex_s = ROOT.TLatex(0.17,0.83,'%s'%label_(sip_))
    latex_s.SetNDC()
    latex_s.SetTextSize(0.035)
    latex_s.SetTextFont(42)
    return latex_s


def latex_bar(bar_):
    latex_b = ROOT.TLatex(0.19,0.65,'bar%02d'%bar_)
    latex_b.SetNDC()
    latex_b.SetTextSize(0.035)
    latex_b.SetTextFont(42)
    return latex_b
# ----------------

#set the tdr style
tdrstyle.setTDRStyle()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetLabelSize(0.055,'X')
ROOT.gStyle.SetLabelSize(0.055,'Y')
ROOT.gStyle.SetTitleSize(0.06,'X')
ROOT.gStyle.SetTitleSize(0.06,'Y')
ROOT.gStyle.SetTitleOffset(1.05,'X')
ROOT.gStyle.SetTitleOffset(1.12,'Y')
ROOT.gStyle.SetLegendFont(42)
ROOT.gStyle.SetLegendTextSize(0.045)
ROOT.gStyle.SetPadTopMargin(0.07)
ROOT.gStyle.SetPadRightMargin(0.1)

ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.SetBatch(False)
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0111)
    
# =====================================




plotsdir = '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/'

marker_code = True
color_code = True
compareToModel = False


verbose = True


# types
if compareNum == 1:
    sipmTypes = ['HPK_nonIrr_LYSO818','HPK_nonIrr_LYSO813','HPK_nonIrr_LYSO816']
    nameComparison = 'HPK_nonIrr_angle64_T5C_types'
    extraLabel = ['','','']
    extraName = ['_angle64_T5C', '_angle64_T5C', '_angle64_T5C']


# angles
elif compareNum == 2:
    sipmTypes = ['HPK_nonIrr_LYSO818', 'HPK_nonIrr_LYSO818', 'HPK_nonIrr_LYSO818']
    nameComparison = 'HPK_nonIrr_LYSO818_T5C_angles'
    extraLabel = [' 32^{o}',' 52^{o}', ' 64^{o}']
    extraName = ['_angle32_T5C', '_angle52_T5C','_angle64_T5C',]


# sipm cell sizes
elif compareNum == 3:
    sipmTypes = ['HPK_nonIrr_LYSO820', 'HPK_nonIrr_LYSO813', 'HPK_nonIrr_LYSO528']
    nameComparison = 'HPK_nonIrr_angle52_T5C_cellSizes'
    extraLabel = ['', '', '']
    extraName = ['_angle52_T5C', '_angle52_T5C', '_angle52_T5C']

#--------------------------------------------------------------------------------------







if color_code:
    #color_map = [632, 600, 416]
    color_map = [806,896,613,886,597,866,429,846,816,413,629,397,590,611,795,1,2,3,4,5,6,7,8,9,10,11]
if marker_code:
    marker_map = [20,20,20,20,20,20,20,20]



outFileName = plotsdir+'/plot_tRes_'+nameComparison+'.root'
outfile = ROOT.TFile(outFileName, 'RECREATE')

sipm_base = {}

for it,sipm in enumerate(sipmTypes):
    sipmTypes[it] = sipm + extraName[it]
    sipm_base[it] = sipm


if verbose:
    print 'sipmTypes: ', sipmTypes , '\t outfile: ', outFileName
#---------






#--------------------------------------------------------------------------------------

# ----- output --------
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/test_slewrate/%s/'%nameComparison

if (os.path.exists(outdir)==False):
    os.mkdir(outdir)



# -------- retrieve module infos --------
fnames   = {}
labels   = {}
cols     = {}
markers  = {}
LO       = {}
tau      = {}
tauRise  = {}
NpeFrac  = {}
thick    = {}

for it, sipm in enumerate(sipmTypes):
    fnames[sipm]   = '%s/summaryPlots_%s.root'%(plotsdir,sipm)
    labels[sipm]   = label_(sipm) + extraLabel[it]
    cols[sipm]     = color_map[it]
    markers[sipm]  = marker_map[it]
    LO[sipm]       = light_output(sipm)
    tau[sipm]      = tau_decay(sipm)
    tauRise[sipm]  = tau_rise(sipm)
    NpeFrac[sipm]  = Npe_frac(sipm)
    thick[sipm]    = thickness(sipm)



if compareToModel:
    g_SR_vs_Vov_model = {}
    for it,name in enumerate(SRmodelGraphs):
        SRmodelfile = ROOT.TFile.Open(SRmodelfileName)
        g_SR_vs_Vov_model[sipmTypes[it]] = SRmodelfile.Get(name)



if verbose:
    print 'defining graphs'
np         = 3
errSRsyst  = 0.10 # error on the slew rate
errPDE     = 0.05 # assumed uncertainty on PDE (5-10%)


g_data = {}
g_data_average = {}



if verbose:
    print 'retrieving bars and ovs'

# --- retrieve bars and ovs from summary plots
bars = {}
Vovs = {}
for sipm in sipmTypes:
    f = ROOT.TFile.Open(fnames[sipm])
    print sipm, fnames[sipm]
    listOfKeys = [key.GetName().replace('g_deltaT_totRatioCorr_bestTh_vs_vov_','') for key in ROOT.gDirectory.GetListOfKeys() if ( 'g_deltaT_totRatioCorr_bestTh_vs_vov_bar' in key.GetName())]
    bars[sipm] = []
    for k in listOfKeys:
        bars[sipm].append( int(k[3:5]) )
    listOfKeys2 = [key.GetName().replace('g_deltaT_totRatioCorr_bestTh_vs_bar_','') for key in ROOT.gDirectory.GetListOfKeys() if key.GetName().startswith('g_deltaT_totRatioCorr_bestTh_vs_bar_')]
    Vovs[sipm] = []
    for k in listOfKeys2:
        Vovs[sipm].append( float(k[3:7]) )
    print bars[sipm]
    print Vovs[sipm]


VovsUnion = []
barsUnion = []
barsIntersection = []
for it, sipm in enumerate(sipmTypes):
    if it == 0:
        VovsUnion = Vovs[sipm]
        barsUnion = bars[sipm]
        barsIntersection = bars[sipm]
    else:
        VovsUnion = union(VovsUnion, Vovs[sipm]) 
        barsUnion = union(barsUnion, bars[sipm])
        barsIntersection = intersection(barsIntersection, bars[sipm])
print '\novs union: ', VovsUnion, '\t bars union: ', barsUnion

# ------   





f      = {}
fPS    = {}
Npe    = {}
gain   = {}

##################
for it,sipm in enumerate(sipmTypes):
    f[sipm] = ROOT.TFile.Open(fnames[sipm])
    if not f[sipm]:
        print 'summary plot file not found'

    g_data_average[sipm] = f[sipm].Get('g_deltaT_totRatioCorr_bestTh_vs_vov_enBin01_average')
    Npe[sipm]                = {}
    gain[sipm]               = {}

    g_data[sipm]             = {}


    if verbose:
        print 'retrieving pulse shapes'

    fPS[sipm] = {}
    for ov in Vovs[sipm]:
        fPS[sipm][ov] = ROOT.TFile.Open('%s/pulseShape_%s_Vov%.2f%s.root'%(plotsdir,sipm_base[it],ov,extraName[it]))
        if not fPS[sipm][ov]:
            print 'pulse shape file not found'
    if verbose:
        print 'retrieving summary plots'

    for bar in bars[sipm]:
        g_data[sipm][bar] = f[sipm].Get('g_deltaT_totRatioCorr_bestTh_vs_vov_bar%02d_enBin01'%bar)

        if verbose:
            print '\n check sipm ', sipm , '  bar ', bar
            for ipoint in range(g_data[sipm][bar].GetN()):
                print 'tres ', g_data[sipm][bar].GetPointY(ipoint), '  ov: ', g_data[sipm][bar].GetPointX(ipoint)
            if g_data[sipm][bar].GetN == 0:
                print 'no point found in summary plot' 


        # loop over ovs 
        for ov in Vovs[sipm]:

            if verbose:
                print("\nov: ", ov)
            s_meas = g_data[sipm][bar].Eval(ov)
            indref = [i for i in range(0, g_data[sipm][bar].GetN()) if g_data[sipm][bar].GetPointX(i) == ov]
            if ( len(indref)<1 ): continue
            err_s_meas = g_data[sipm][bar].GetErrorY(indref[0])
            Npe[sipm][ov]  = 4.2*LO[sipm]*NpeFrac[sipm]*PDE_(ov,sipm)/PDE_(3.5,sipm,'0')
            gain[sipm][ov] = Gain_(ov,sipm)
            g_psL = fPS[sipm][ov].Get('g_pulseShapeL_bar%02d_Vov%.2f'%(bar,ov))
            g_psR = fPS[sipm][ov].Get('g_pulseShapeR_bar%02d_Vov%.2f'%(bar,ov))
            if (g_psL==None): continue
            if (g_psR==None): continue
            g_psL.SetName('g_pulseShapeL_bar%02d_Vov%.2f_%s'%(bar,ov,sipm))
            g_psR.SetName('g_pulseShapeR_bar%02d_Vov%.2f_%s'%(bar,ov,sipm))
            timingThreshold = findTimingThreshold(f[sipm].Get('g_deltaT_totRatioCorr_vs_th_bar%02d_Vov%.2f_enBin01'%(bar,ov)))
            srL = -1
            srR = -1
            sr = -1
            err_srL = -1
            err_srR = -1

            # draw pulse shape
            c = ROOT.TCanvas('c_%s_%s'%(g_psL.GetName().replace('g_pulseShapeL','pulseShape'),sipm),'',600,500)  
            hdummy = ROOT.TH2F('hdummy','', 100, min(g_psL.GetX())-1., 5., 100, 0., 15.)
            hdummy.GetXaxis().SetTitle('time [ns]')
            hdummy.GetYaxis().SetTitle('amplitude [#muA]')
            hdummy.Draw()
            gtempL = ROOT.TGraphErrors()
            gtempR = ROOT.TGraphErrors()
            srL,err_srL = getSlewRateFromPulseShape(g_psL, timingThreshold, np, gtempL, c)
            srR,err_srR = getSlewRateFromPulseShape(g_psR, timingThreshold, np, gtempR, c) 
            line = ROOT.TLine(min(g_psL.GetX())-1., timingThreshold*0.313, 30., timingThreshold*0.313)
            line.SetLineStyle(7)
            line.SetLineWidth(2)
            line.SetLineColor(ROOT.kOrange+1)        
            line.Draw('same')

            # labels
            lat_s = latex_sipm(sipm)
            lat_s.Draw()
            lat = latex_vov(ov)
            lat.Draw()
            lat_b = latex_bar(bar)
            lat_b.Draw()
            c.SaveAs(outdir+c.GetName()+'.png')   
            hdummy.Delete()

