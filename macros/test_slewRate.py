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
from SiPM import *
from moduleDict import *





# ------------------ FUNZIONI -------------------------
# ============================================================================
def getSlewRateFromPulseShape(g1, timingThreshold, npoints, gtemp, canvas=None):
    if ( g1.GetN() < npoints): 
        return (-1, -1)
    print 'NUMBER OF POINTS : ', g1.GetN()

    # find index at the timing threshold
    itiming = 0
    for i in range(0,g1.GetN()):
        if (round(g1.GetY()[i]/0.313) == timingThreshold):
            itiming = i
            break

    ifirst = ROOT.TMath.LocMin(g1.GetN(), g1.GetX())
    imin = max(0, itiming-2)

    if ( imin >= 0 and g1.GetX()[imin+1] < g1.GetX()[imin] ): imin = ifirst

    tmin = g1.GetX()[imin]
    tmax = 3
    
    if ((imin+npoints) < g1.GetN()): 
        tmax = min(g1.GetX()[imin+npoints],max(g1.GetX()))
        nmax = imin+npoints+1
    else:
        tmax = max(g1.GetX())
        nmax = g1.GetN()-1

    print 'tmax: ', tmax,'   nmax: ', nmax

    for i in range(imin, nmax):
        gtemp.SetPoint(gtemp.GetN(), g1.GetX()[i], g1.GetY()[i])
        gtemp.SetPointError(gtemp.GetN()-1, g1.GetErrorX(i), g1.GetErrorY(i))
    fitSR = ROOT.TF1('fitSR', 'pol1', tmin, tmax)
    fitSR.SetLineColor(g1.GetMarkerColor()+1)
    fitSR.SetRange(tmin,tmax)
    fitSR.SetParameters(0, 10)
    fitStatus = int(gtemp.Fit(fitSR, 'QRS+'))
    sr = fitSR.Derivative( g1.GetX()[itiming])
    err_sr = fitSR.GetParError(1)
    if (canvas!=None):
        canvas.cd()
        gtemp.SetMarkerStyle(g1.GetMarkerStyle())
        gtemp.SetMarkerColor(g1.GetMarkerColor())
        gtemp.Draw('psames')
        g1.Draw('psames')
        fitSR.Draw('same')
        canvas.Update()
        #ps = g1.FindObject("stats")
        ps = gtemp.FindObject("stats")
        ps.SetTextColor(g1.GetMarkerColor())
        if ('L' in g1.GetName()):
            ps.SetY1NDC(0.85) # new y start position
            ps.SetY2NDC(0.95)# new y end position
        if ('R' in g1.GetName()):
            ps.SetY1NDC(0.73) # new y start position
            ps.SetY2NDC(0.83)# new y end position
    return(sr,err_sr)


def findTimingThreshold(g2,ov):
    xmin = 0
    ymin = 9999
    for i in range(0, g2.GetN()):
        y = g2.GetY()[i]
        x = g2.GetX()[i]
        if ( y < ymin):
            ymin = y
            xmin = x 
    return xmin


def sigma_noise(sr):
    noise_single = math.sqrt( pow(420./sr,2) + 16.7*16.7 )
    return noise_single / math.sqrt(2)

def getTimeResolution(h1_deltaT):
    tRes = [-1,-1]
    h1_deltaT.GetXaxis().SetRangeUser(h1_deltaT.GetMean() - 5*h1_deltaT.GetRMS(), h1_deltaT.GetMean() + 5*h1_deltaT.GetRMS())
    fitFunc = ROOT.TF1('fitFunc','gaus',-10000, 10000)
    fitFunc.SetLineColor(ROOT.kGreen+3)
    fitFunc.SetLineWidth(2)
    fitFunc.SetParameters(h1_deltaT.GetMaximum(),h1_deltaT.GetMean(), h1_deltaT.GetRMS())
    fitXMin = h1_deltaT.GetBinCenter(h1_deltaT.GetMaximumBin()) - 200
    fitXMax = h1_deltaT.GetBinCenter(h1_deltaT.GetMaximumBin()) + 200.
    fitFunc.SetRange(fitXMin, fitXMax)
    h1_deltaT.Fit('fitFunc','QNRL','', fitXMin, fitXMax)
    fitFunc.SetRange(fitFunc.GetParameter(1) - 1.0*fitFunc.GetParameter(2), fitFunc.GetParameter(1) + 1.0*fitFunc.GetParameter(2))
    h1_deltaT.Fit('fitFunc','QNRL')
    fitFunc.SetRange(fitFunc.GetParameter(1) - 2.5*fitFunc.GetParameter(2), fitFunc.GetParameter(1) + 2.5*fitFunc.GetParameter(2))
    h1_deltaT.Fit('fitFunc','QRSL+')
    tRes = [ fitFunc.GetParameter(2),fitFunc.GetParError(2)]
    return tRes
# ====================================












###############
comparisonNum = 4
###############

    
# =====================================



#plotsdir = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/'
plotsdir = '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/'

# ------------------ 
if comparisonNum == 4:
    modules =       ['LYSO819',   'LYSO817']
    temperatures =  ['-22',       '-22']
    extraName =     ['_angle64',  '_angle64']
    extraLabel =    ['',          '']
    outSuffix =     'test'
    color_code =    True




# ------------------ 


verbose = False
sipmTypes = []
sipmBase = []

for it,module in enumerate(modules):
    sipmTypes.append(sipm_(module)+'_'+lyso_(module)+extraName[it]+'_T'+temperatures[it]+'C')
    print 'test: ', sipmTypes[it], '   temp : ', temperatures[it]
    sipmBase.append(sipm_(module)+'_'+lyso_(module))


#color_map = [208,212,216,224,227,94,225,99,220]
color_map = [2,210,4,6,7,8,94]



# ----- output --------
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_May23/plot_tRes/%s/'%outSuffix

if (os.path.exists(outdir)==False):
    os.mkdir(outdir)
if (os.path.exists(outdir+'/pulseShape')==False):
    os.mkdir(outdir+'/pulseShape/')




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
    markers[sipm]  = 20
    LO[sipm]       = light_output(sipm)
    tau[sipm]      = tau_decay(sipm)
    tauRise[sipm]  = tau_rise(sipm)
    NpeFrac[sipm]  = Npe_frac(sipm)
    thick[sipm]    = thickness(sipm)






if verbose:
    print 'defining graphs'
np         = 3
errSRsyst  = 0.10 # error on the slew rate
errPDE     = 0.05 # assumed uncertainty on PDE (5-10%)


g_data = {}
g_data_average = {}


# --- retrieve bars and ovs from moduleChar plots
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

    if 'HPK_2E14_LYSO825' in sipm:
        Vovs[sipm].remove(0.6) # too small signals for reasonable SR fits
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

    fPS[sipm] = {}
    for ov in Vovs[sipm]:
        fPS[sipm][ov] = ROOT.TFile.Open('%s/pulseShape_%s_Vov%.2f%s_T%sC.root'%(plotsdir,sipmBase[it],ov,extraName[it],temperatures[it]))
        if not fPS[sipm][ov]:
            print 'pulse shape file not found'

    for bar in bars[sipm]:
        g_data[sipm][bar] = f[sipm].Get('g_deltaT_totRatioCorr_bestTh_vs_vov_bar%02d_enBin01'%bar)

        if verbose:
            print '\n check sipm ', sipm , '  bar ', bar
            for ipoint in range(g_data[sipm][bar].GetN()):
                print 'tres ', g_data[sipm][bar].GetPointY(ipoint), '  ov: ', g_data[sipm][bar].GetPointX(ipoint)

    # --- loop on ov ----        g_data = tRes vs vov
        for ov in Vovs[sipm]:
            ovEff = Vovs_eff(sipm, ov)

            # --- get measured t_res
            s_data = g_data[sipm][bar].Eval(ovEff)
            indref = [i for i in range(0, g_data[sipm][bar].GetN()) if g_data[sipm][bar].GetPointX(i) == ovEff]
            if ( len(indref)<1 ): continue
            err_s_data = g_data[sipm][bar].GetErrorY(indref[0])            
            
            # Npe and Gain at this OVeff
            Npe[sipm][ov]  = 4.2*LO[sipm]*NpeFrac[sipm]*PDE_(ovEff,sipm)/PDE_(3.5,sipm,'0') 
            gain[sipm][ov] = Gain_(ovEff,sipm)

            # get pulse shapes
            g_psL = fPS[sipm][ov].Get('g_pulseShapeL_bar%02d_Vov%.2f'%(bar,ov))
            g_psR = fPS[sipm][ov].Get('g_pulseShapeR_bar%02d_Vov%.2f'%(bar,ov))
            if (g_psL==None and g_psR==None): continue
            if (g_psL!=None): g_psL.SetName('g_pulseShapeL_bar%02d_Vov%.2f_%s'%(bar,ov,sipm))
            if (g_psR!=None): g_psR.SetName('g_pulseShapeR_bar%02d_Vov%.2f_%s'%(bar,ov,sipm))
            timingThreshold = findTimingThreshold(f[sipm].Get('g_deltaT_energyRatioCorr_vs_th_bar%02d_Vov%.2f_enBin01'%(bar,ov)), ovEff)
            srL     = -1
            srR     = -1
            sr      = -1
            err_srL = -1
            err_srR = -1
            c = ROOT.TCanvas('c_%s'%(g_psL.GetName().replace('g_pulseShapeL','pulseShape').replace('Vov%.2f'%ov,'VovEff%.2f'%ovEff)),'',650,500)  
            hdummy = ROOT.TH2F('hdummy','', 100, min(g_psL.GetX())-1., 5, 100, 0., 15.)
            hdummy.GetXaxis().SetTitle('time [ns]')
            hdummy.GetYaxis().SetTitle('amplitude [#muA]')
            hdummy.Draw()
            gtempL = ROOT.TGraphErrors()
            gtempR = ROOT.TGraphErrors()
            
            if ( ov == 0.60 and 'LYSO825' in sipm): np = 2 # reduce npoints for SR fit
            else: np = 3
            if (g_psL!=None): 
                srL,err_srL = getSlewRateFromPulseShape(g_psL, timingThreshold, np, gtempL, c)
            if (g_psR!=None): 
                srR,err_srR = getSlewRateFromPulseShape(g_psR, timingThreshold, np, gtempR, c) 
            line = ROOT.TLine(min(g_psL.GetX())-1., timingThreshold*0.313, 30., timingThreshold*0.313)
            line.SetLineStyle(7)
            line.SetLineWidth(2)
            line.SetLineColor(ROOT.kOrange+1)        
            line.Draw('same')

            # ---- some labels ----
            latex = ROOT.TLatex(0.17,0.83,'%s'%label_(sipm))
            latex.SetNDC()
            latex.SetTextSize(0.035)
            latex.SetTextFont(42)
            latex.Draw('same')
            latexVov = ROOT.TLatex(0.19,0.75,'Vov%.2f'%ov)
            latexVov.SetNDC()
            latexVov.SetTextSize(0.035)
            latexVov.SetTextFont(42)
            latexVov.Draw('same')
            latexBar = ROOT.TLatex(0.19,0.65,'bar%02d'%bar)
            latexBar.SetNDC()
            latexBar.SetTextSize(0.035)
            latexBar.SetTextFont(42)
            latexBar.Draw('same')

            c.SaveAs(outdir+'/pulseShape/'+c.GetName()+'.png')   
            hdummy.Delete()
