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

comparisonNum = int(args.comparisonNumber)

#-------------


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



plotsdir = '/eos/home-s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/plots/'

compareToModel = False
color_code = True

# ---T1 T2 T3  52 degree ----- 
if comparisonNum == 1:
    modules       = ['LYSO818',  'LYSO813',  'LYSO816']
    temperatures  = ['12',       '12',       '12']
    extraName     = ['_angle52', '_angle52', '_angle52']
    extraLabel    = [' - T1',' - T2',' - T3']
    outSuffix     = 'nonIrr_T1_T2_T3_angle52'

    SRmodelfileName = 'slewRate_vs_Vov_model.root'
    SRmodelGraphs = ['g_SR_vs_Vov_HPK_25um_ES2_type1', 'g_SR_vs_Vov_HPK_25um_ES2_type2', 'g_SR_vs_Vov_HPK_25um_ES2_type3']
    compareToModel = True




# --- RUs T1 T1 T1 -----
elif comparisonNum == 2:
    modules       = ['LYSO818',  'LYSO818',  'LYSO818']
    temperatures  = ['12',       '12',       '12']
    extraName     = ['_angle32', '_angle52', '_angle64']
    extraLabel    = [' - T1 - 32^{o}',' - T1 - 52^{o}',' - T1 - 64^{o}']
    outSuffix     = 'nonIrr_T1_T1_T1'


# -- RUs T1 T2 T2 -----
elif comparisonNum == 3:
    modules       = ['LYSO818',  'LYSO813',  'LYSO813']
    temperatures  = ['12',       '12',       '12']
    extraName     = ['_angle32', '_angle52', '_angle64']
    extraLabel    = [' - T1 - 32^{o}',' - T2 - 52^{o}',' - T2 - 64^{o}']
    outSuffix     = 'nonIrr_T1_T2_T2'
    color_code = True



# -- RUs T1 T2 T3 -----
elif comparisonNum == 4:
    modules       = ['LYSO818',  'LYSO813',  'LYSO816']
    temperatures  = ['12',       '12',       '12']
    extraName     = ['_angle32', '_angle52', '_angle52']
    extraLabel    = [' - T1 - 32^{o}',' - T2 - 52^{o}',' - T3 - 52^{o}']
    outSuffix     = 'nonIrr_T1_T2_T3*'





# --- cell size -----
elif comparisonNum == 5:
    modules        = ['LYSO528'   , 'LYSO814' ,  'LYSO813'  ,  'LYSO820']
    temperatures   = ['12',         '12' ,       '12',         '5']
    extraName      = ['_angle52',   '_angle52',  '_angle52',   '_angle52']
    extraLabel     = ['',           '',          '',           '']
    outSuffix      = 'nonIrr_cellSizes'







verbose = False

if len(modules) != len(temperatures):
    print 'ERROR: either one LYSO or temperature is missing'
    sys.exit()

sipmTypes = []
sipmBase = []

outFileName = plotsdir+'/plot_tRes_'+outSuffix+'.root'
outfile = ROOT.TFile(outFileName, 'RECREATE')

for it,module in enumerate(modules):
    sipmTypes.append(sipm_(module)+'_'+lyso_(module)+extraName[it]+'_T'+temperatures[it]+'C')
    print 'test: ', sipmTypes[it], '   temp : ', temperatures[it]
    sipmBase.append(sipm_(module)+'_'+lyso_(module))


if verbose:
    print 'module: ', sipmTypes , '\t outfile: ', outfile

#color_map = [208,212,216,224,227,94,225,99,220]
if color_code:
    color_map = [2,210,4,6,7,8,94]








#--------------------------------------------------------------------------------------

# ----- output --------
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_FNAL_Mar23/plot_tRes/%s/'%outSuffix

if (os.path.exists(outdir)==False):
    os.mkdir(outdir)
if (os.path.exists(outdir+'/pulseShape')==False):
    os.mkdir(outdir+'/pulseShape/')
if (os.path.exists(outdir+'/bestTh')==False):
    os.mkdir(outdir+'/bestTh/')

if (os.path.exists(outdir+'/slewRate_vs_Vov_perBar')==False):
    os.mkdir(outdir+'/slewRate_vs_Vov_perBar/')

if (os.path.exists(outdir+'/slewRate_vs_bar_perVov')==False):
    os.mkdir(outdir+'/slewRate_vs_bar_perVov/')

if (os.path.exists(outdir+'/slewRate_vs_GainNpe_perBar')==False):
    os.mkdir(outdir+'/slewRate_vs_GainNpe_perBar/')


if (os.path.exists(outdir+'/tRes_vs_bar_perVov')==False):
    os.mkdir(outdir+'/tRes_vs_bar_perVov/')

if (os.path.exists(outdir+'/tRes_vs_Vov_perBar')==False):
    os.mkdir(outdir+'/tRes_vs_Vov_perBar/')

if (os.path.exists(outdir+'/tRes_vs_slewRate')==False):
    os.mkdir(outdir+'/tRes_vs_slewRate/')







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


# ------ vs Vov -----
g_Noise_vs_Vov     = {}
g_Stoch_vs_Vov     = {}
g_StochExp_vs_Vov    = {}
g_TotExp_vs_Vov    = {}


g_bestTh_vs_Vov    = {}
g_SR_vs_Vov        = {}
g_Npe_vs_Vov       = {}


# ------ vs Npe / Gain -----
g_Stoch_vs_Npe     = {}
g_data_vs_Npe      = {}

g_SR_vs_GainNpe    = {}
g_data_vs_GainNpe  = {}

# ------ vs bar -----
g_bestTh_vs_bar    = {}
g_SR_vs_bar        = {}
g_Noise_vs_bar     = {}
g_Stoch_vs_bar     = {}
g_StochExp_vs_bar     = {}
g_TotExp_vs_bar       = {}

# --- vs SR
g_data_vs_SR        = {}
g_Stoch_vs_SR      = {}
g_Noise_vs_SR      = {}


g_data_vs_staticPower = {}


if verbose:
    print 'retrieving bars and ovs'

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
print 'ovs union: ', VovsUnion, '\t bars union: ', barsUnion

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

    g_Npe_vs_Vov[sipm]       = ROOT.TGraphErrors()
    g_Noise_vs_Vov[sipm]     = {}
    g_Stoch_vs_Vov[sipm]     = {}
    g_StochExp_vs_Vov[sipm]     = {}
    g_TotExp_vs_Vov[sipm]     = {}

    g_SR_vs_Vov[sipm]        = {}
    g_bestTh_vs_Vov[sipm]    = {}

    g_Stoch_vs_Npe[sipm]     = {}
    g_data_vs_Npe[sipm]      = ROOT.TGraphErrors()
    g_SR_vs_GainNpe[sipm]    = {}
    g_data_vs_GainNpe[sipm]  = ROOT.TGraphErrors()

    g_SR_vs_bar[sipm]        = {}
    g_bestTh_vs_bar[sipm]    = {}
    g_Noise_vs_bar[sipm]     = {}
    g_Stoch_vs_bar[sipm]     = {}
    g_StochExp_vs_bar[sipm]     = {}
    g_TotExp_vs_bar[sipm]       = {}

    g_Stoch_vs_SR[sipm] = {}
    g_Noise_vs_SR[sipm] = {}
    g_data_vs_SR[sipm] = {}

    g_data_vs_Npe[sipm] = ROOT.TGraphErrors()
    g_data_vs_staticPower[sipm] = ROOT.TGraphErrors()
    g_data_vs_GainNpe[sipm] = ROOT.TGraphErrors()


    if verbose:
        print 'retrieving pulse shapes'

    fPS[sipm] = {}
    for ov in Vovs[sipm]:
        fPS[sipm][ov] = ROOT.TFile.Open('%s/pulseShape_%s_Vov%.2f%s_T%sC.root'%(plotsdir,sipmBase[it],ov,extraName[it],temperatures[it]))
        if not fPS[sipm][ov]:
            print 'pulse shape file not found'

        g_SR_vs_bar[sipm][ov]        = ROOT.TGraphErrors()
        g_bestTh_vs_bar[sipm][ov]    = ROOT.TGraphErrors()
        g_Noise_vs_bar[sipm][ov]     = ROOT.TGraphErrors()
        g_Stoch_vs_bar[sipm][ov]     = ROOT.TGraphErrors()
        g_StochExp_vs_bar[sipm][ov]       = ROOT.TGraphErrors()
        g_TotExp_vs_bar[sipm][ov]       = ROOT.TGraphErrors()
        g_Stoch_vs_SR[sipm][ov]      = ROOT.TGraphErrors()
        g_Noise_vs_SR[sipm][ov]      = ROOT.TGraphErrors()
        g_data_vs_SR[sipm][ov]        = ROOT.TGraphErrors()

    if verbose:
        print 'retrieving summary plots'

    for bar in bars[sipm]:
        g_data[sipm][bar] = f[sipm].Get('g_deltaT_totRatioCorr_bestTh_vs_vov_bar%02d_enBin01'%bar)

        if verbose:
            print '\n check sipm ', sipm , '  bar ', bar
            for ipoint in range(g_data[sipm][bar].GetN()):
                print 'tres ', g_data[sipm][bar].GetPointY(ipoint), '  ov: ', g_data[sipm][bar].GetPointX(ipoint)

        g_Noise_vs_Vov[sipm][bar]     = ROOT.TGraphErrors()
        g_Stoch_vs_Vov[sipm][bar]     = ROOT.TGraphErrors()
        g_StochExp_vs_Vov[sipm][bar]    = ROOT.TGraphErrors()
        g_TotExp_vs_Vov[sipm][bar]    = ROOT.TGraphErrors()

        g_Stoch_vs_Npe[sipm][bar]     = ROOT.TGraphErrors()

        g_SR_vs_Vov[sipm][bar]        = ROOT.TGraphErrors()
        g_SR_vs_GainNpe[sipm][bar]    = ROOT.TGraphErrors()
        g_bestTh_vs_Vov[sipm][bar]    = ROOT.TGraphErrors()
        

        if verbose:
            print 'starting loop on ov'







    # --- loop on ov ----        g_data = tRes vs vov  ------> for ov reference only!
        for ov in Vovs[sipm]:
            ovEff = Vovs_eff(sipm, ov)
            if ovEff != ov_reference(sipm):      #  here I want to compute the stochastic term of 3.5 V ov only
                continue
            # --- get measured t_res
            s_data = g_data[sipm][bar].Eval(ovEff)
            indref = [i for i in range(0, g_data[sipm][bar].GetN()) if g_data[sipm][bar].GetPointX(i) == ovEff]
            if ( len(indref)<1 ): continue
            err_s_data = g_data[sipm][bar].GetErrorY(indref[0])            
            # get pulse shapes
            g_psL = fPS[sipm][ov].Get('g_pulseShapeL_bar%02d_Vov%.2f'%(bar,ov))
            g_psR = fPS[sipm][ov].Get('g_pulseShapeR_bar%02d_Vov%.2f'%(bar,ov))
            if (g_psL==None and g_psR==None): continue
            if (g_psL!=None): g_psL.SetName('g_pulseShapeL_bar%02d_Vov%.2f_%s'%(bar,ov,sipm))
            if (g_psR!=None): g_psR.SetName('g_pulseShapeR_bar%02d_Vov%.2f_%s'%(bar,ov,sipm))
            timingThreshold = findTimingThreshold(f[sipm].Get('g_deltaT_energyRatioCorr_vs_th_bar%02d_Vov%.2f_enBin01'%(bar,ov)), ovEff)
            gtempL = ROOT.TGraphErrors()
            gtempR = ROOT.TGraphErrors()
            np = 3
            srL,err_srL = getSlewRateFromPulseShape(g_psL, timingThreshold, np, gtempL)
            srR,err_srR = getSlewRateFromPulseShape(g_psR, timingThreshold, np, gtempR)
            if (srL>0 and srR>0):
                # weighted average
                sr =  ( (srL/(err_srL*err_srL) + srR/(err_srR*err_srR) ) / (1./(err_srL*err_srL) + 1./(err_srR*err_srR) ) )
                errSR = 1./math.sqrt( 1./(err_srL*err_srL)  +  1./(err_srR*err_srR) )
                errSR = errSR/sr
            elif (srL>0 and srR<0):
                sr = srL
                errSR = err_srL/sr
            elif (srL<0 and srR>0):
                sr = srR
                errSR = err_srR/sr
            if (ov<=1.5):
                errSRsyst = 0.2
            else:
                errSRsyst = 0.1
            errSR = math.sqrt(errSR*errSR+errSRsyst*errSRsyst) 

            if (s_data>=sigma_noise(sr)): # this is for ov reference !
                s_stoch_ref = math.sqrt(s_data*s_data - sigma_noise(sr)*sigma_noise(sr))
                err_sigma_noise = 0.5*(sigma_noise(sr*(1-errSR))-sigma_noise(sr*(1+errSR)))
                err_s_stoch_ref = 1./s_stoch_ref*math.sqrt( pow(err_s_data*s_data,2)+pow( sigma_noise(sr)*err_sigma_noise ,2) )
            else:
                print 'skipping bar%02d:  %.1f   %.1f'%(bar, s_data,sigma_noise(sr))
                continue
                













    # second loop over ALL ovs



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

            # draw Pulse shape
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




            if (srL>0 and srR>0):
                # weighted average
                sr =  ( (srL/(err_srL*err_srL) + srR/(err_srR*err_srR) ) / (1./(err_srL*err_srL) + 1./(err_srR*err_srR) ) )
                errSR = 1./math.sqrt( 1./(err_srL*err_srL)  +  1./(err_srR*err_srR) )
                errSR = errSR
            if (srL>0 and srR<0):
                sr = srL
                errSR = err_srL
            if (srL<0 and srR>0):
                sr = srR
                errSR = err_srR
            if (srL<0 and srR<0): continue
            errSR = math.sqrt(errSR*errSR+errSRsyst*errSRsyst*sr*sr) 

            g_Npe_vs_Vov[sipm].SetPoint(g_Npe_vs_Vov[sipm].GetN(), ovEff, Npe[sipm][ov])

            g_SR_vs_Vov[sipm][bar].SetPoint( g_SR_vs_Vov[sipm][bar].GetN(), ovEff, sr )
            g_SR_vs_Vov[sipm][bar].SetPointError( g_SR_vs_Vov[sipm][bar].GetN()-1, 0, errSR )
            
            g_SR_vs_GainNpe[sipm][bar].SetPoint( g_SR_vs_GainNpe[sipm][bar].GetN(), gain[sipm][ov]*Npe[sipm][ov], sr )
            g_SR_vs_GainNpe[sipm][bar].SetPointError( g_SR_vs_GainNpe[sipm][bar].GetN()-1, 0, errSR )

            g_bestTh_vs_Vov[sipm][bar].SetPoint( g_bestTh_vs_Vov[sipm][bar].GetN(), ovEff, timingThreshold )
            g_bestTh_vs_Vov[sipm][bar].SetPointError( g_bestTh_vs_Vov[sipm][bar].GetN()-1, 0, 0 )
            
            g_SR_vs_bar[sipm][ov].SetPoint( g_SR_vs_bar[sipm][ov].GetN(), bar, sr )
            g_SR_vs_bar[sipm][ov].SetPointError( g_SR_vs_bar[sipm][ov].GetN()-1, 0, errSR )
            
            g_bestTh_vs_bar[sipm][ov].SetPoint( g_bestTh_vs_bar[sipm][ov].GetN(), bar, timingThreshold )
            g_bestTh_vs_bar[sipm][ov].SetPointError( g_bestTh_vs_bar[sipm][ov].GetN()-1, 0, 0)


            s_noise = sigma_noise(sr)
            err_s_noise =  0.5*(sigma_noise(sr*(1-errSR/sr))-sigma_noise(sr*(1+errSR/sr)))


            g_Noise_vs_bar[sipm][ov].SetPoint( g_Noise_vs_bar[sipm][ov].GetN(), bar, s_noise )
            g_Noise_vs_bar[sipm][ov].SetPointError( g_Noise_vs_bar[sipm][ov].GetN()-1, 0,  err_s_noise)
            
            g_Noise_vs_Vov[sipm][bar].SetPoint(g_Noise_vs_Vov[sipm][bar].GetN(), ovEff, s_noise)
            g_Noise_vs_Vov[sipm][bar].SetPointError(g_Noise_vs_Vov[sipm][bar].GetN()-1, 0, err_s_noise)
            
            g_data_vs_SR[sipm][ov].SetPoint(g_data_vs_SR[sipm][ov].GetN(), sr, s_data)
            g_data_vs_SR[sipm][ov].SetPointError(g_data_vs_SR[sipm][ov].GetN()-1, errSR, err_s_data)

            g_Noise_vs_SR[sipm][ov].SetPoint(g_Noise_vs_SR[sipm][ov].GetN(), sr, s_noise)
            g_Noise_vs_SR[sipm][ov].SetPointError(g_Noise_vs_SR[sipm][ov].GetN()-1, errSR, err_s_noise)

            if (s_data > s_noise):
                s_stoch = math.sqrt(s_data*s_data-s_noise*s_noise)
                err_s_stoch = 1./s_stoch * math.sqrt( pow(s_data*err_s_data, 2)  +  pow(s_noise*g_Noise_vs_Vov[sipm][bar].GetErrorY(g_Noise_vs_Vov[sipm][bar].GetN()-1),2) )

                g_Stoch_vs_Npe[sipm][bar].SetPoint(g_Stoch_vs_Npe[sipm][bar].GetN(), Npe[sipm][ov], s_stoch)
                g_Stoch_vs_Npe[sipm][bar].SetPointError(g_Stoch_vs_Npe[sipm][bar].GetN()-1, 0, err_s_stoch)

                g_Stoch_vs_Vov[sipm][bar].SetPoint(g_Stoch_vs_Vov[sipm][bar].GetN(), ovEff, s_stoch)
                g_Stoch_vs_Vov[sipm][bar].SetPointError(g_Stoch_vs_Vov[sipm][bar].GetN()-1, 0, err_s_stoch)

                g_Stoch_vs_bar[sipm][ov].SetPoint( g_Stoch_vs_bar[sipm][ov].GetN(), bar, s_stoch )
                g_Stoch_vs_bar[sipm][ov].SetPointError( g_Stoch_vs_bar[sipm][ov].GetN()-1, 0,  err_s_stoch)

                g_Stoch_vs_SR[sipm][ov].SetPoint(g_Stoch_vs_SR[sipm][ov].GetN(), sr, s_stoch)
                g_Stoch_vs_SR[sipm][ov].SetPointError(g_Stoch_vs_SR[sipm][ov].GetN()-1, errSR, err_s_stoch)

            # compute expected stochastic term  by scaling from 3.5 V OV    
            s_stoch_exp = s_stoch_ref / math.sqrt( PDE_(ovEff,sipm)/PDE_(ov_reference(sipm),sipm)  )
            err_s_stoch_exp = err_s_stoch_ref/math.sqrt( PDE_(ovEff, sipm)/PDE_(ov_reference(sipm), sipm) )

            g_StochExp_vs_Vov[sipm][bar].SetPoint(g_StochExp_vs_Vov[sipm][bar].GetN(), ov, s_stoch_exp)
            g_StochExp_vs_Vov[sipm][bar].SetPointError(g_StochExp_vs_Vov[sipm][bar].GetN()-1, 0, err_s_stoch_exp)

            g_StochExp_vs_bar[sipm][ov].SetPoint(g_StochExp_vs_bar[sipm][ov].GetN(), bar, s_stoch_exp)
            g_StochExp_vs_bar[sipm][ov].SetPointError(g_StochExp_vs_bar[sipm][ov].GetN()-1, 0, err_s_stoch_exp)

            # tot resolution summing noise + stochastic (scaled) in quadrature
            s_tot_exp = math.sqrt( s_stoch_exp*s_stoch_exp + s_noise*s_noise )
            err_s_tot_exp = 1./s_tot_exp * math.sqrt( pow( err_s_stoch_exp*s_stoch_exp,2) + pow(s_noise*g_Noise_vs_Vov[sipm][bar].GetErrorY(g_Noise_vs_Vov[sipm][bar].GetN()-1),2))

            g_TotExp_vs_Vov[sipm][bar].SetPoint(g_TotExp_vs_Vov[sipm][bar].GetN(), ov, s_tot_exp)
            g_TotExp_vs_Vov[sipm][bar].SetPointError(g_TotExp_vs_Vov[sipm][bar].GetN()-1, 0, err_s_tot_exp)

            g_TotExp_vs_bar[sipm][ov].SetPoint(g_TotExp_vs_bar[sipm][ov].GetN(), bar, s_tot_exp)
            g_TotExp_vs_bar[sipm][ov].SetPointError(g_TotExp_vs_bar[sipm][ov].GetN()-1, 0, err_s_tot_exp)



            # -----------------------------------------------------------------------------




if verbose:
    print 'computing average graphs'


#  ----------------------------------------
#  -------------- average -----------------

g_SR_vs_Vov_average = {}
g_Noise_vs_Vov_average = {}
g_Stoch_vs_Vov_average = {}

g_TotExp_vs_Vov_average = {}


for sipm in sipmTypes:
    g_SR_vs_Vov_average[sipm]     = ROOT.TGraphErrors()
    g_Noise_vs_Vov_average[sipm]  = ROOT.TGraphErrors()
    g_Stoch_vs_Vov_average[sipm]  = ROOT.TGraphErrors()
    g_TotExp_vs_Vov_average[sipm] = ROOT.TGraphErrors()

    for ov in Vovs[sipm]:
        ovEff = Vovs_eff(sipm, ov) 
        staticCurrent = float(current_(sipm,ov)) * 1E-03
        staticPower = staticCurrent * (37. + ovEff) * 1000.    # in mW

        if (ov in  g_SR_vs_bar[sipm].keys()): 

            # average SR
            fitpol0_sr = ROOT.TF1('fitpol0_sr','pol0',-100,100)
            if (g_SR_vs_bar[sipm][ov].GetN()==0): continue;
            g_SR_vs_bar[sipm][ov].Fit(fitpol0_sr,'QNR')
            sr = fitpol0_sr.GetParameter(0)
            g_SR_vs_Vov_average[sipm].SetPoint(g_SR_vs_Vov_average[sipm].GetN(), ovEff, sr)
            g_SR_vs_Vov_average[sipm].SetPointError(g_SR_vs_Vov_average[sipm].GetN()-1, 0, fitpol0_sr.GetParError(0))

            # noise using average SR
            g_Noise_vs_Vov_average[sipm].SetPoint(g_Noise_vs_Vov_average[sipm].GetN(), ovEff, sigma_noise(sr))
            sr_err = max(fitpol0_sr.GetParError(0), errSRsyst*sr)
            sr_up   = sr + sr_err 
            sr_down = sr - sr_err 
            noise_err  = 0.5 * ( sigma_noise(sr_down) - sigma_noise(sr_up) ) 
            g_Noise_vs_Vov_average[sipm].SetPointError(g_Noise_vs_Vov_average[sipm].GetN()-1, 0, noise_err) 
    
            # average stochastic 
            fitpol0_stoch = ROOT.TF1('fitpol0_stoch','pol0',-100,100)  
            g_Stoch_vs_bar[sipm][ov].Fit(fitpol0_stoch,'QNR')
            s_stoch = fitpol0_stoch.GetParameter(0)
            err_s_stoch = g_Stoch_vs_bar[sipm][ov].GetRMS(2)/math.sqrt(16) # fixme!
            g_Stoch_vs_Vov_average[sipm].SetPoint(g_Stoch_vs_Vov_average[sipm].GetN(), ovEff, s_stoch)
            g_Stoch_vs_Vov_average[sipm].SetPointError(g_Stoch_vs_Vov_average[sipm].GetN()-1, 0, err_s_stoch)

            # tot resolution summing noise + expected stochastic in quadrature
            fitpol0_stoch_exp = ROOT.TF1('fitpol0_stoch_exp','pol0',-100,100)
            g_StochExp_vs_bar[sipm][ov].Fit(fitpol0_stoch_exp,'QNR')
            s_stoch_exp = fitpol0_stoch_exp.GetParameter(0)
            err_s_stoch_exp = g_StochExp_vs_bar[sipm][ov].GetRMS(2)/math.sqrt(16)
        
            tot = math.sqrt( s_stoch_exp*s_stoch_exp + sigma_noise(sr)*sigma_noise(sr) )
            err_tot = 1./tot * math.sqrt( pow( err_s_stoch_exp*s_stoch_exp,2) + pow(noise_err*sigma_noise(sr),2) )

            g_TotExp_vs_Vov_average[sipm].SetPoint(g_TotExp_vs_Vov_average[sipm].GetN(), ovEff, tot)
            g_TotExp_vs_Vov_average[sipm].SetPointError(g_TotExp_vs_Vov_average[sipm].GetN()-1, 0, err_tot)

            

            # average tRes vs Npe, static power, GainNpe            
            fitpol0 = ROOT.TF1('fitpol0','pol0',-100,100)
            gg = f[sipm].Get('g_deltaT_totRatioCorr_bestTh_vs_bar_Vov%.02f_enBin01'%ov)    
            gg.Fit(fitpol0,'QNR')
            g_data_vs_Npe[sipm].SetPoint(g_data_vs_Npe[sipm].GetN(), Npe[sipm][ov], fitpol0.GetParameter(0))
            g_data_vs_Npe[sipm].SetPointError(g_data_vs_Npe[sipm].GetN()-1, 0, fitpol0.GetParError(0))

            g_data_vs_staticPower[sipm].SetPoint(g_data_vs_staticPower[sipm].GetN(), staticPower, fitpol0.GetParameter(0))
            g_data_vs_staticPower[sipm].SetPointError(g_data_vs_staticPower[sipm].GetN()-1, 0,  fitpol0.GetParError(0))

            g_data_vs_GainNpe[sipm].SetPoint(g_data_vs_GainNpe[sipm].GetN(), gain[sipm][ov]*Npe[sipm][ov], fitpol0.GetParameter(0))
            g_data_vs_GainNpe[sipm].SetPointError(g_data_vs_GainNpe[sipm].GetN()-1, 0, fitpol0.GetParError(0))






#----------------------------------------------------------------------------------
# ratio of stochatic terms at 3.5 OV
g_ratio_stoch1 = ROOT.TGraphErrors()
g_ratio_stoch2 = ROOT.TGraphErrors()
g_ratio_stoch3 = ROOT.TGraphErrors()
for bar in range(0,16):
    if (bar not in bars[sipmTypes[1]]): continue
    if (bar not in bars[sipmTypes[0]]): continue
    if (g_Stoch_vs_Vov[sipmTypes[0]][bar].Eval(3.5)<=0): continue
    ratio_stoch =  g_Stoch_vs_Vov[sipmTypes[1]][bar].Eval(3.5)/g_Stoch_vs_Vov[sipmTypes[0]][bar].Eval(3.5)
    err1 = [  g_Stoch_vs_Vov[sipmTypes[1]][bar].GetErrorY(i) for i in range(0, g_Stoch_vs_Vov[sipmTypes[1]][bar].GetN()) if g_Stoch_vs_Vov[sipmTypes[1]][bar].GetX()[i] == 3.50]
    err0 = [  g_Stoch_vs_Vov[sipmTypes[0]][bar].GetErrorY(i) for i in range(0, g_Stoch_vs_Vov[sipmTypes[0]][bar].GetN()) if g_Stoch_vs_Vov[sipmTypes[0]][bar].GetX()[i] == 3.50]
    if (err1 == [] or err0 == []): continue
    err_ratio_stoch = ratio_stoch * math.sqrt( pow(err1[0]/g_Stoch_vs_Vov[sipmTypes[1]][bar].Eval(3.5),2) + pow(err0[0]/g_Stoch_vs_Vov[sipmTypes[0]][bar].Eval(3.5),2) ) 
    if verbose:
        print sipmTypes[1], sipmTypes[0], ' ratio stochastic term at 3.5 V OV = ', ratio_stoch
    g_ratio_stoch1.SetPoint(g_ratio_stoch1.GetN(), bar, ratio_stoch)
    g_ratio_stoch1.SetPointError(g_ratio_stoch1.GetN()-1, 0, err_ratio_stoch)

for bar in range(0,16):
    if (bar not in bars[sipmTypes[1]]): continue
    if (bar not in bars[sipmTypes[2]]): continue
    if (g_Stoch_vs_Vov[sipmTypes[2]][bar].Eval(3.5)<=0): continue
    if (g_Stoch_vs_Vov[sipmTypes[1]][bar].Eval(3.5)<=0): continue
    ratio_stoch =  g_Stoch_vs_Vov[sipmTypes[1]][bar].Eval(3.5)/g_Stoch_vs_Vov[sipmTypes[2]][bar].Eval(3.5)
    err1 = [  g_Stoch_vs_Vov[sipmTypes[1]][bar].GetErrorY(i) for i in range(0, g_Stoch_vs_Vov[sipmTypes[1]][bar].GetN()) if g_Stoch_vs_Vov[sipmTypes[1]][bar].GetX()[i] == 3.50]
    err0 = [  g_Stoch_vs_Vov[sipmTypes[2]][bar].GetErrorY(i) for i in range(0, g_Stoch_vs_Vov[sipmTypes[2]][bar].GetN()) if g_Stoch_vs_Vov[sipmTypes[2]][bar].GetX()[i] == 3.50]
    if (err1 == [] or err0 == []): continue
    err_ratio_stoch = ratio_stoch * math.sqrt( pow(err1[0]/g_Stoch_vs_Vov[sipmTypes[1]][bar].Eval(3.5),2) + pow(err0[0]/g_Stoch_vs_Vov[sipmTypes[2]][bar].Eval(3.5),2) ) 
    if verbose:
        print sipmTypes[1], sipmTypes[2],' ratio stochastic term at 3.5 V OV = ', ratio_stoch
    g_ratio_stoch2.SetPoint(g_ratio_stoch2.GetN(), bar, ratio_stoch)
    g_ratio_stoch2.SetPointError(g_ratio_stoch2.GetN()-1, 0, err_ratio_stoch)



for bar in range(0,16):
    if (bar not in bars[sipmTypes[0]]): continue
    if (bar not in bars[sipmTypes[2]]): continue
    if (g_Stoch_vs_Vov[sipmTypes[2]][bar].Eval(3.5)<=0): continue
    if (g_Stoch_vs_Vov[sipmTypes[0]][bar].Eval(3.5)<=0): continue
    ratio_stoch =  g_Stoch_vs_Vov[sipmTypes[0]][bar].Eval(3.5)/g_Stoch_vs_Vov[sipmTypes[2]][bar].Eval(3.5)
    err1 = [  g_Stoch_vs_Vov[sipmTypes[0]][bar].GetErrorY(i) for i in range(0, g_Stoch_vs_Vov[sipmTypes[0]][bar].GetN()) if g_Stoch_vs_Vov[sipmTypes[0]][bar].GetX()[i] == 3.50]
    err0 = [  g_Stoch_vs_Vov[sipmTypes[2]][bar].GetErrorY(i) for i in range(0, g_Stoch_vs_Vov[sipmTypes[2]][bar].GetN()) if g_Stoch_vs_Vov[sipmTypes[2]][bar].GetX()[i] == 3.50]
    if (err1 == [] or err0 == []): continue
    err_ratio_stoch = ratio_stoch * math.sqrt( pow(err1[0]/g_Stoch_vs_Vov[sipmTypes[0]][bar].Eval(3.5),2) + pow(err0[0]/g_Stoch_vs_Vov[sipmTypes[2]][bar].Eval(3.5),2) ) 
    if verbose:
        print sipmTypes[0], sipmTypes[2],' ratio stochastic term at 3.5 V OV = ', ratio_stoch
    g_ratio_stoch3.SetPoint(g_ratio_stoch3.GetN(), bar, ratio_stoch)
    g_ratio_stoch3.SetPointError(g_ratio_stoch3.GetN()-1, 0, err_ratio_stoch)
        

























if verbose:
    print '\n\nstart drawing'



####################
###### draw
###################


leg = {}

# Tres vs OV
print('Plotting time resolution vs OV...')
for sipm in sipmTypes:
    leg[sipm] = ROOT.TLegend(0.65,0.60,0.89,0.79)
    leg[sipm].SetBorderSize(0)
    leg[sipm].SetFillStyle(0)
    for i,bar in enumerate(bars[sipm]):
        if (bar not in g_data[sipm].keys()): continue
        if (g_data[sipm][bar].GetN()==0): continue
        c =  ROOT.TCanvas('c_timeResolution_vs_Vov_%s_bar%02d'%(sipm,bar),'c_timeResolution_vs_Vov_%s_bar%02d'%(sipm,bar),650,500)
        c.SetGridy()
        c.cd()
        xmin = 0.0
        xmax = 4.0
        hdummy = ROOT.TH2F('hdummy_%s_%d'%(sipm,bar),'',100,xmin,xmax,140,0,140)
        hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
        hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
        hdummy.Draw()

        g_data[sipm][bar].SetMarkerStyle(20)
        g_data[sipm][bar].SetMarkerSize(1)
        g_data[sipm][bar].SetMarkerColor(1)
        g_data[sipm][bar].SetLineColor(1)
        g_data[sipm][bar].SetLineWidth(2)
        g_data[sipm][bar].Draw('plsame')
        if (bar not in g_Noise_vs_Vov[sipm].keys()): continue

        g_Noise_vs_Vov[sipm][bar].SetLineWidth(2)
        g_Noise_vs_Vov[sipm][bar].SetLineColor(ROOT.kBlue)
        g_Noise_vs_Vov[sipm][bar].SetFillColor(ROOT.kBlue)
        g_Noise_vs_Vov[sipm][bar].SetFillColorAlpha(ROOT.kBlue,0.5)
        g_Noise_vs_Vov[sipm][bar].SetFillStyle(3004)
        g_Noise_vs_Vov[sipm][bar].Draw('E3lsame')

        g_Stoch_vs_Vov[sipm][bar].SetLineWidth(2)
        g_Stoch_vs_Vov[sipm][bar].SetLineColor(ROOT.kGreen+2)
        g_Stoch_vs_Vov[sipm][bar].SetFillColor(ROOT.kGreen+2)
        g_Stoch_vs_Vov[sipm][bar].SetFillStyle(3001)
        g_Stoch_vs_Vov[sipm][bar].SetFillColorAlpha(ROOT.kGreen+2,0.5)
        g_Stoch_vs_Vov[sipm][bar].Draw('E3lsame')

        g_TotExp_vs_Vov[sipm][bar].SetLineWidth(2)
        g_TotExp_vs_Vov[sipm][bar].SetLineColor(ROOT.kRed+1)
        g_TotExp_vs_Vov[sipm][bar].SetFillColor(ROOT.kRed+1)
        g_TotExp_vs_Vov[sipm][bar].SetFillColorAlpha(ROOT.kRed+1,0.5)
        g_TotExp_vs_Vov[sipm][bar].SetFillStyle(3001)

        #save on file
        outfile.cd()
        g_data[sipm][bar].Write('g_Data_vs_Vov_%s_bar%02d'%(sipm,  bar))
        g_Noise_vs_Vov[sipm][bar].Write('g_Noise_vs_Vov_%s_bar%02d'%(sipm, bar))
        g_Stoch_vs_Vov[sipm][bar].Write('g_Stoch_vs_Vov_%s_bar%02d'%(sipm, bar))

        if (i==0):
            leg[sipm].AddEntry(g_data[sipm][bar], 'data', 'PL')
            leg[sipm].AddEntry(g_Noise_vs_Vov[sipm][bar], 'noise', 'L')
            leg[sipm].AddEntry(g_Stoch_vs_Vov[sipm][bar], 'stoch', 'L')

        leg[sipm].Draw('same')

        latex = ROOT.TLatex(0.20,0.85,'%s'%(sipm.replace('_',' ').replace('T','T=')))
        latex.SetNDC()
        latex.SetTextSize(0.045)
        latex.SetTextFont(42)
        latex.Draw('same')

        cms_logo = draw_logo()
        cms_logo.Draw()

        c.SaveAs(outdir+'/tRes_vs_Vov_perBar/'+c.GetName()+'.png')
        c.SaveAs(outdir+'/tRes_vs_Vov_perBar/'+c.GetName()+'.pdf')
        hdummy.Delete()


# -----------   vs npe  ----------------


# SR and best threshold vs Vov
leg2 = ROOT.TLegend(0.20,0.70,0.45,0.89)
leg2.SetBorderSize(0)
leg2.SetFillStyle(0)

    
bar = barsIntersection[0]
for sipm in sipmTypes:
    leg2.AddEntry(g_SR_vs_Vov[sipm][bar], '%s'%labels[sipm], 'PL')

#i = 0
for bar in range(0,16):
    if (bar not in g_data[sipm].keys()): continue
    if (g_data[sipm][bar].GetN()==0): continue     
    c = ROOT.TCanvas('c_slewRate_vs_Vov_bar%02d'%(bar),'c_slewRate_vs_Vov_bar%02d'%(bar),650,500)
    c.SetGridy()
    c.cd()
    xmin = 0.0
    xmax = 4.0
    ymax = 35
    hdummy = ROOT.TH2F('hdummy_%d'%(bar),'',100,xmin,xmax,100,0,ymax)
    hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
    hdummy.GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
    hdummy.Draw()
    for sipm in sipmTypes:
        #if (i==0):
          #  leg2.AddEntry(g_SR_vs_Vov[sipm][bar], '%s'%labels[sipm], 'PL')
        if (bar not in g_SR_vs_Vov[sipm].keys()): continue
        g_SR_vs_Vov[sipm][bar].SetMarkerStyle(markers[sipm])
        g_SR_vs_Vov[sipm][bar].SetMarkerColor(cols[sipm])
        g_SR_vs_Vov[sipm][bar].SetLineColor(cols[sipm])
        g_SR_vs_Vov[sipm][bar].Draw('plsame')
    leg2.Draw()
    outfile.cd()
    g_SR_vs_Vov[sipm][bar].Write('g_SR_vs_Vov_%s_bar%02d'%(sipm,bar))
    c.SaveAs(outdir+'/slewRate_vs_Vov_perBar/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/slewRate_vs_Vov_perBar/'+c.GetName()+'.pdf')
    hdummy.Delete()
    i=i+1


    c = ROOT.TCanvas('c_slewRate_vs_GainNpe_bar%02d'%(bar),'c_slewRate_vs_GainNpe_bar%02d'%(bar),650,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%d'%(bar),'',100,0,3E09,100,0,35)
    hdummy.GetXaxis().SetTitle('gain x Npe')
    hdummy.GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
    hdummy.Draw()
    for sipm in sipmTypes:
        if (bar not in g_SR_vs_GainNpe[sipm].keys()): continue
        g_SR_vs_GainNpe[sipm][bar].SetMarkerStyle( markers[sipm] )
        g_SR_vs_GainNpe[sipm][bar].SetMarkerColor(cols[sipm])
        g_SR_vs_GainNpe[sipm][bar].SetLineColor(cols[sipm])
        g_SR_vs_GainNpe[sipm][bar].Draw('psame')
    leg2.Draw()

    cms_logo = draw_logo()
    cms_logo.Draw()
    c.SaveAs(outdir+'/slewRate_vs_GainNpe_perBar/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/slewRate_vs_GainNpe_perBar/'+c.GetName()+'.pdf')
    hdummy.Delete()

    c = ROOT.TCanvas('c_bestTh_vs_Vov_bar%02d'%(bar),'c_bestTh_vs_Vov_bar%02d'%(bar),650,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%d'%(bar),'',100,xmin,xmax,100,0,20)
    hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
    hdummy.GetYaxis().SetTitle('best threshold [DAC]')
    hdummy.Draw()
    

    for sipm in sipmTypes:
        if (bar not in g_bestTh_vs_Vov[sipm].keys()): continue
        g_bestTh_vs_Vov[sipm][bar].SetMarkerStyle(markers[sipm])
        g_bestTh_vs_Vov[sipm][bar].SetMarkerColor(cols[sipm])
        g_bestTh_vs_Vov[sipm][bar].SetLineColor(cols[sipm])
        g_bestTh_vs_Vov[sipm][bar].Draw('plsame')

    cms_logo = draw_logo()
    cms_logo.Draw()
    c.SaveAs(outdir+'/bestTh/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/bestTh/'+c.GetName()+'.pdf')
    hdummy.Delete()






# average slew rate vs OV
c =  ROOT.TCanvas('c_slewRate_vs_Vov_average','c_slewRate_vs_Vov_average',650,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',16, 0.0, 4.0 ,100, 0,35)
hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
hdummy.GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
hdummy.Draw()
for sipm in sipmTypes:
    g_SR_vs_Vov_average[sipm].SetMarkerStyle(markers[sipm])
    g_SR_vs_Vov_average[sipm].SetMarkerColor(cols[sipm])
    g_SR_vs_Vov_average[sipm].SetLineWidth(1)
    g_SR_vs_Vov_average[sipm].SetLineColor(cols[sipm])
    g_SR_vs_Vov_average[sipm].Draw('plsame')
    outfile.cd()
    g_SR_vs_Vov_average[sipm].Write('g_SR_vs_Vov_average_%s'%(sipm))
leg2.Draw()

cms_logo = draw_logo()
cms_logo.Draw()
c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()







# average time resolution vs Npe
c =  ROOT.TCanvas('c_timeResolution_vs_Npe_average','c_timeResolution_vs_Npe_average',650,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',1000, 1000, 6000, 100, 20, 140)
hdummy.GetXaxis().SetTitle('Npe')
hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
hdummy.GetXaxis().SetNdivisions(505)
hdummy.Draw()
for sipm in sipmTypes:
    g_data_vs_Npe[sipm].SetMarkerStyle(markers[sipm])
    g_data_vs_Npe[sipm].SetMarkerColor(cols[sipm])
    g_data_vs_Npe[sipm].SetLineWidth(1)
    g_data_vs_Npe[sipm].SetLineColor(cols[sipm])
    g_data_vs_Npe[sipm].Draw('plsame')
    outfile.cd()
    g_data_vs_Npe[sipm].Write('g_data_vs_Npe_average_%s'%(sipm))
leg2.Draw()  

cms_logo = draw_logo()
cms_logo.Draw()
c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()


# average time resolution vs static power   ----------> NON AVEVAMO LE CORRENTI <---------------------------------------
c =  ROOT.TCanvas('c_timeResolution_vs_staticPower_average','c_timeResolution_vs_staticPower_average',650,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',1000, 0, 120, 100, 0, 120)
hdummy.GetXaxis().SetTitle('static power [mW]')


hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
hdummy.Draw()
for sipm in sipmTypes:
    g_data_vs_staticPower[sipm].SetMarkerStyle(markers[sipm])
    g_data_vs_staticPower[sipm].SetMarkerColor(cols[sipm])
    g_data_vs_staticPower[sipm].SetLineWidth(1)
    g_data_vs_staticPower[sipm].SetLineColor(cols[sipm])
    g_data_vs_staticPower[sipm].Draw('plsame')
    outfile.cd()
#    g_data_vs_staticPower[sipm].Write('g_data_vs_staticPower_average_%s'%(sipm))
leg2.Draw()  
cms_logo = draw_logo()
cms_logo.Draw()
#c.SaveAs(outdir+'/'+c.GetName()+'.png')
#c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()





# average time resolution vs GainxNpe
c =  ROOT.TCanvas('c_timeResolution_vs_GainNpe_average','c_timeResolution_vs_GainNpe_average',650,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',1000, 0, 3E09, 100, 20, 140)
hdummy.GetXaxis().SetTitle('Gain x Npe')
hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
hdummy.GetXaxis().SetNdivisions(505)
hdummy.Draw()
for sipm in sipmTypes:
    g_data_vs_GainNpe[sipm].SetMarkerStyle(markers[sipm])
    g_data_vs_GainNpe[sipm].SetMarkerColor(cols[sipm])
    g_data_vs_GainNpe[sipm].SetLineWidth(1)
    g_data_vs_GainNpe[sipm].SetLineColor(cols[sipm])
    g_data_vs_GainNpe[sipm].Draw('plsame')
leg2.Draw()  
cms_logo = draw_logo()
cms_logo.Draw()
c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()
                                       

# average tRes
for sipm in sipmTypes:
    latex = ROOT.TLatex(0.18,0.88,'%s'%(labels[sipm]))
    latex.SetNDC()
    latex.SetTextSize(0.05)
    latex.SetTextFont(42)
    c =  ROOT.TCanvas('c_timeResolution_vs_Vov_average_%s'%(sipm),'c_timeResolution_vs_Vov_average_%s'%(sipm),650,500)
    c.SetGridx()
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy','',100, 0., 4.,100,0,120)
    hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
    hdummy.GetYaxis().SetTitle('time resolution [ps]')
    hdummy.Draw()
    g_data_average[sipm].SetMarkerStyle(20)
    g_data_average[sipm].SetMarkerSize(1)
    g_data_average[sipm].SetMarkerColor(1)
    g_data_average[sipm].SetLineColor(1)
    g_data_average[sipm].SetLineWidth(2)
    g_data_average[sipm].Draw('plsame')

    g_Noise_vs_Vov_average[sipm].SetLineWidth(2)
    g_Noise_vs_Vov_average[sipm].SetLineColor(ROOT.kBlue)
    g_Noise_vs_Vov_average[sipm].SetFillColor(ROOT.kBlue)
    g_Noise_vs_Vov_average[sipm].SetFillColorAlpha(ROOT.kBlue,0.5)
    g_Noise_vs_Vov_average[sipm].SetFillStyle(3004)
    g_Noise_vs_Vov_average[sipm].Draw('E3lsame')
    g_Stoch_vs_Vov_average[sipm].SetLineWidth(2)
    g_Stoch_vs_Vov_average[sipm].SetLineColor(ROOT.kGreen+2)
    g_Stoch_vs_Vov_average[sipm].SetFillColor(ROOT.kGreen+2)
    g_Stoch_vs_Vov_average[sipm].SetFillStyle(3001)
    g_Stoch_vs_Vov_average[sipm].SetFillColorAlpha(ROOT.kGreen+2,0.5)
    g_Stoch_vs_Vov_average[sipm].Draw('E3lsame')
    g_TotExp_vs_Vov_average[sipm].SetLineWidth(2)
    g_TotExp_vs_Vov_average[sipm].SetLineColor(ROOT.kRed+1)
    g_TotExp_vs_Vov_average[sipm].SetFillColor(ROOT.kRed+1)
    g_TotExp_vs_Vov_average[sipm].SetFillColorAlpha(ROOT.kRed+1,0.5)
    g_TotExp_vs_Vov_average[sipm].SetFillStyle(3001)
    #g_TotExp_vs_Vov_average[sipm].Draw('E3lsame')
    leg[sipm].Draw()

    latex.Draw()
    outfile.cd()
    g_Noise_vs_Vov_average[sipm].Write('g_Noise_vs_Vov_average_%s'%sipm)
    g_Stoch_vs_Vov_average[sipm].Write('g_Stoch_vs_Vov_average_%s'%sipm)
    g_TotExp_vs_Vov_average[sipm].Write('g_Tot_vs_Vov_average_%s'%sipm)

    cms_logo = draw_logo()
    cms_logo.Draw()
    c.SaveAs(outdir+'/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
    hdummy.Delete()


# SR and best threshold vs bar
for sipm in sipmTypes:
    for ov in Vovs[sipm]:
        if (ov not in g_SR_vs_bar[sipm].keys()): continue
        ovEff = Vovs_eff(sipm, ov)        
        c = ROOT.TCanvas('c_slewRate_vs_bar_%s_Vov%.2f'%(sipm,ovEff),'c_slewRate_vs_bar_%s_Vov%.2f'%(sipm,ovEff),650,500)
        c.SetGridy()
        c.cd()
        #hdummy = ROOT.TH2F('hdummy5_%d'%(ov),'',100,-0.5,15.5,100,0,15)
        hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,-0.5,15.5,100,0,35)
        hdummy.GetXaxis().SetTitle('bar')
        hdummy.GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
        hdummy.Draw()
        g_SR_vs_bar[sipm][ov].SetMarkerStyle(markers[sipm])
        g_SR_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])

        g_SR_vs_bar[sipm][ov].SetLineColor(cols[sipm])
        g_SR_vs_bar[sipm][ov].Draw('psame')
        leg2.Draw()
        c.SaveAs(outdir+'/slewRate_vs_bar_perVov/'+c.GetName()+'.png')
        c.SaveAs(outdir+'/slewRate_vs_bar_perVov/'+c.GetName()+'.pdf')
        hdummy.Delete()

        c = ROOT.TCanvas('c_bestTh_vs_bar_%s_Vov%.2f'%(sipm,ovEff),'c_bestTh_vs_bar_%s_Vov%.2f'%(sipm,ovEff),650,500)
        c.SetGridy()
        c.cd()
        hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,-0.5,15.5,100,0,20)
        hdummy.GetXaxis().SetTitle('bar')
        hdummy.GetYaxis().SetTitle('timing threshold [DAC]')
        hdummy.Draw()
        g_bestTh_vs_bar[sipm][ov].SetMarkerStyle(markers[sipm])
        g_bestTh_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])
        g_bestTh_vs_bar[sipm][ov].SetLineColor(cols[sipm])
        g_bestTh_vs_bar[sipm][ov].Draw('plsame')
        leg2.Draw()        
        c.SaveAs(outdir+'/bestTh/'+c.GetName()+'.png')
        c.SaveAs(outdir+'/bestTh/'+c.GetName()+'.pdf')
        hdummy.Delete()





#------- vs SR -------
for sipm in sipmTypes:
    for ov in Vovs[sipm]:
        if (ov not in g_Stoch_vs_SR[sipm].keys()): continue
        ovEff = Vovs_eff(sipm, ov)        
        c = ROOT.TCanvas('c_stoch_vs_SR_%s_Vov%.2f'%(sipm,ovEff),'c_stoch_vs_SR_%s_Vov%.2f'%(sipm,ovEff),650,500)
        c.SetGridy()
        c.cd()
        hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,0,35.5,100,0,60)
        hdummy.GetXaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
        hdummy.GetYaxis().SetTitle('#sigma_{stoch} [ps]')
        hdummy.Draw()

        g_Stoch_vs_SR[sipm][ov].SetMarkerStyle(markers[sipm])
        g_Stoch_vs_SR[sipm][ov].SetMarkerColor(cols[sipm])
        g_Stoch_vs_SR[sipm][ov].SetLineColor(cols[sipm])
        g_Stoch_vs_SR[sipm][ov].Draw('psame')

        leg2.Draw()
        c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.png')
        c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.pdf')
        hdummy.Delete()


        c = ROOT.TCanvas('c_noise_vs_SR_%s_Vov%.2f'%(sipm,ovEff),'c_noise_vs_SR_%s_Vov%.2f'%(sipm,ovEff),650,500)
        c.SetGridy()
        c.cd()
        hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,0,35,100,0,60)
        hdummy.GetXaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
        hdummy.GetYaxis().SetTitle('#sigma_{noise} [ps]')
        hdummy.Draw()

        g_Noise_vs_SR[sipm][ov].SetMarkerStyle(markers[sipm])
        g_Noise_vs_SR[sipm][ov].SetMarkerColor(cols[sipm])
        g_Noise_vs_SR[sipm][ov].SetLineColor(cols[sipm])
        g_Noise_vs_SR[sipm][ov].Draw('plsame')
        leg2.Draw()        
        c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.png')
        c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.pdf')
        hdummy.Delete()

        c = ROOT.TCanvas('c_data_vs_SR_%s_Vov%.2f'%(sipm,ovEff),'c_data_vs_SR_%s_Vov%.2f'%(sipm,ovEff),650,500)
        c.SetGridy()
        c.cd()
        hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,-0.5,15.5,100,0,140)
        hdummy.GetXaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
        hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
        hdummy.Draw()

        g_data_vs_SR[sipm][ov].SetMarkerStyle( markers[sipm] )
        g_data_vs_SR[sipm][ov].SetMarkerColor(cols[sipm])
        g_data_vs_SR[sipm][ov].SetLineColor(cols[sipm])
        g_data_vs_SR[sipm][ov].Draw('psame')
        leg2.Draw()
        c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.png')
        c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.pdf')
        hdummy.Delete()







# --- stoch and noise term vs bar - all sipms on same canvas
for ov in VovsUnion:
    c = ROOT.TCanvas('c_noise_vs_bar_Vov%.2f'%(ov),'c_noise_vs_bar_Vov%.2f'%(ov),650,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_Vov%.2f'%(ov),'',100,-0.5,15.5,100,0,80)
    hdummy.GetXaxis().SetTitle('bar')
    hdummy.GetYaxis().SetTitle('#sigma_{t, noise} [ps]')
    hdummy.Draw()
    for j, sipm in enumerate(sipmTypes):
        if ov not in g_Noise_vs_bar[sipm].keys():
            continue
        g_Noise_vs_bar[sipm][ov].SetMarkerStyle( markers[sipm] )
        g_Noise_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])
        g_Noise_vs_bar[sipm][ov].SetLineColor(cols[sipm])
        g_Noise_vs_bar[sipm][ov].Draw('psame')
    leg2.Draw()
    c.SaveAs(outdir+'/tRes_vs_bar_perVov/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/tRes_vs_bar_perVov/'+c.GetName()+'.pdf')
    hdummy.Delete()

    c = ROOT.TCanvas('c_stoch_vs_bar_Vov%.2f'%(ov),'c_stoch_vs_bar_Vov%.2f'%(ov),650,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_Vov%.2f'%(ov),'',100,-0.5,15.5,100,0,80)
    hdummy.GetXaxis().SetTitle('bar')
    hdummy.GetYaxis().SetTitle('#sigma_{t, stoch} [ps]')
    hdummy.Draw()
    for j, sipm in enumerate(sipmTypes):
        if ov not in g_Stoch_vs_bar[sipm].keys():
            continue
        g_Stoch_vs_bar[sipm][ov].SetMarkerStyle( markers[sipm] )
        g_Stoch_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])
        g_Stoch_vs_bar[sipm][ov].SetLineColor(cols[sipm])
        g_Stoch_vs_bar[sipm][ov].Draw('psame')
    leg2.Draw()
    c.SaveAs(outdir+'/tRes_vs_bar_perVov/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/tRes_vs_bar_perVov/'+c.GetName()+'.pdf')
    hdummy.Delete()



outfile.Close()
