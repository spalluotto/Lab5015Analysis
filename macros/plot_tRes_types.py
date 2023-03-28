#! /usr/bin/env python

#script che prende pulse shape e risoluzione alla best Th vs Vov --> calcola slew rate, termine di noise dato lo slew rate e calcola lo stocastico come diff in quadratura di tot - noise

#NB: ho una risoluzione temporale calcolata come somma in quadratura di noise e stocastico stimato scalando lo stocastico a 3.5 con la PDE ---> Tot_vs_Vov
# -  tutti gli altri Tot sono la tRes effettivamente misurata
# -  Stoch vs Npe = tRes misurata - noise in quadratura,  mentre stoch vs Vov dato dallo stocastico a 3.5 scalato per PDE
# -  sigma_noise = una funzione che si calcola il noise dato lo slew rate



import os
import shutil
import glob
import math
import array
import sys
import time
import argparse

import ROOT

from SiPM import *
from slewRate import *
from moduleDict import *

ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.SetBatch(False)
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0111)


#--------CAMBIA QUI------------------------------------------------------------------

comparisonNum = 1

if comparisonNum == 1:
    sipmTypes = ['HPK_nonIrr_C25_LYSO818','HPK_nonIrr_C25_LYSO813','HPK_nonIrr_C25_LYSO816']
    outSuffix = 'types_HPK_nonIrr_C25'
    extraLabel = ['','','']
    extraName = ['','','']


#--------------------------------------------------------------------------------------







# ----- output --------
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_FNAL_Mar23/plot_tRes/%s/'%outSuffix

if (os.path.exists(outdir)==False):
    os.mkdir(outdir)
if (os.path.exists(outdir+'/plotsSR')==False):
    os.mkdir(outdir+'/plotsSR/')

outfile = {}

# ----- files ------
#-- temperatures
for it,sipm in enumerate(sipmTypes):
    sipmTypes[it] = sipm + '_T12C' + extraName[it]
    outFileName = '/afs/cern.ch/user/s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/plots/plot_tRes_'+sipmTypes[it]+'.root'
    outfile[sipmTypes[it]] = ROOT.TFile(outFileName, 'RECREATE')

print sipmTypes 
print outfile
#---------



fnames = {}
labels = {}
cols = {}
markers = {}
LO = {}
tau = {}
tauRise = {}
Npe_frac = {}

for it, sipm in enumerate(sipmTypes):
    fnames[sipm] = '../plots/summaryPlots_%s.root'%(sipm)
    labels[sipm] = label_(sipm) + extraLabel[it]
    cols[sipm] = color_(sipm)
    markers[sipm] = 20
    LO[sipm] = light_output(sipm)
    tau[sipm] = tau_decay(sipm)
    tauRise[sipm] = tau_rise(sipm)
    Npe_frac[sipm] = frac(sipm)



np = 3
errSRsyst  = 0.10 # error on the slew rate



g = {}
g_Noise_vs_Vov = {}
g_Stoch_vs_Vov = {}
g_StochMeas_vs_Vov = {}
g_Tot_vs_Vov   = {}

g_Stoch_vs_Npe = {}

g_SR_vs_bar = {}
g_SR_vs_Vov = {}
g_SR_vs_GainNpe = {}

g_bestTh_vs_bar = {}
g_bestTh_vs_Vov = {}

g_Noise_vs_bar = {}
g_Stoch_vs_bar = {}
g_StochMeas_vs_bar = {}
g_Tot_vs_bar = {}

g_Stoch_vs_SR   = {}
g_Noise_vs_SR   = {}
g_Tot_vs_SR   = {}



# --- retrieve bars and ovs from moduleChar plots ---> maybe it is better to consider only good barsrecupero barre e Vov dai nomi dei file

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

    # pero forse e meglio prendere solo le good bars
    bars[sipm] = good_bars(sipm, Vovs[sipm], bars[sipm])


fPS = {}
Npe = {}
g_Npe_vs_Vov = {}

for sipm in sipmTypes:
    f = ROOT.TFile.Open(fnames[sipm])

    Npe[sipm] = {}
    g[sipm] = {}

    g_Npe_vs_Vov[sipm] = ROOT.TGraphErrors()

    g_Noise_vs_Vov[sipm] = {}
    g_Stoch_vs_Vov[sipm] = {}
    g_StochMeas_vs_Vov[sipm] = {}
    g_Tot_vs_Vov[sipm] = {}

    g_Stoch_vs_Npe[sipm] = {}

    g_SR_vs_Vov[sipm] = {}
    g_bestTh_vs_Vov[sipm] = {}

    g_SR_vs_bar[sipm] = {}
    g_bestTh_vs_bar[sipm] = {}
    g_Noise_vs_bar[sipm] = {}
    g_Stoch_vs_bar[sipm] = {}
    g_StochMeas_vs_bar[sipm] = {}
    g_Tot_vs_bar[sipm] = {}
    g_SR_vs_GainNpe[sipm] = {}

    g_Stoch_vs_SR[sipm] = {}
    g_Noise_vs_SR[sipm] = {}
    g_Tot_vs_SR[sipm] = {}

    fPS[sipm] = {}
    for ov in Vovs[sipm]:

        fPS[sipm][ov] = ROOT.TFile.Open('../plots/pulseShape_%s_Vov%.2f.root'%(sipm,ov))

        g_SR_vs_bar[sipm][ov] = ROOT.TGraphErrors()
        g_bestTh_vs_bar[sipm][ov] = ROOT.TGraphErrors()
        g_Noise_vs_bar[sipm][ov] = ROOT.TGraphErrors()
        g_Stoch_vs_bar[sipm][ov] = ROOT.TGraphErrors()
        g_StochMeas_vs_bar[sipm][ov] = ROOT.TGraphErrors()
        g_Tot_vs_bar[sipm][ov] = ROOT.TGraphErrors()
        g_Stoch_vs_SR[sipm][ov] = ROOT.TGraphErrors()
        g_Noise_vs_SR[sipm][ov] = ROOT.TGraphErrors()
        g_Tot_vs_SR[sipm][ov]   = ROOT.TGraphErrors()

    for bar in bars[sipm]:
        #g[sipm][bar] = f.Get('g_deltaT_totRatioCorr_vs_vov_bar%02d_th10_enBin01'%bar)
        g[sipm][bar] = f.Get('g_deltaT_totRatioCorr_bestTh_vs_vov_bar%02d_enBin01'%bar)
        g_Noise_vs_Vov[sipm][bar] = ROOT.TGraphErrors()
        g_Stoch_vs_Vov[sipm][bar] = ROOT.TGraphErrors()
        g_StochMeas_vs_Vov[sipm][bar] = ROOT.TGraphErrors()
        g_Tot_vs_Vov[sipm][bar] = ROOT.TGraphErrors()

        g_Stoch_vs_Npe[sipm][bar] = ROOT.TGraphErrors()

        g_SR_vs_Vov[sipm][bar] = ROOT.TGraphErrors()
        g_SR_vs_GainNpe[sipm][bar] = ROOT.TGraphErrors()
        g_bestTh_vs_Vov[sipm][bar] = ROOT.TGraphErrors()
        
        sigma_stoch_ref = 0
        err_sigma_stoch_ref = 0
        ov_ref = 3.5
    
        for i in range(0,g[sipm][bar].GetN()):
            ov = g[sipm][bar].GetX()[i]
#            print 'ov = ',ov
            if (ov != ov_ref): continue
            sigma_tot = g[sipm][bar].GetY()[i]
            err_sigma_tot = g[sipm][bar].GetErrorY(i)
            g_psL = fPS[sipm][ov].Get('g_pulseShapeL_bar%02d_Vov%.2f'%(bar,ov))
            g_psR = fPS[sipm][ov].Get('g_pulseShapeR_bar%02d_Vov%.2f'%(bar,ov))
            if (g_psL==None): continue
            if (g_psR==None): continue
            g_psL.SetName('g_pulseShapeL_bar%02d_Vov%.2f'%(bar,ov))
            g_psR.SetName('g_pulseShapeR_bar%02d_Vov%.2f'%(bar,ov))
            timingThreshold = findTimingThreshold(f.Get('g_deltaT_totRatioCorr_vs_th_bar%02d_Vov%.2f_enBin01'%(bar,ov)),ov)
            gtempL = ROOT.TGraphErrors()
            gtempR = ROOT.TGraphErrors()
            if (ov == 1.5):
#                print 'np = 2, sono nella condizone ov: ', ov
                np = 1
            else:
#                print 'np = 3, sono nella condizone ov: ', ov
                np = 3
            srL,err_srL = getSlewRateFromPulseShape(g_psL, timingThreshold, np, gtempL)
            srR,err_srR = getSlewRateFromPulseShape(g_psR, timingThreshold, np, gtempR)
            if (srL>0 and srR>0):
                # weighted average
                sr =  ( (srL/(err_srL*err_srL) + srR/(err_srR*err_srR) ) / (1./(err_srL*err_srL) + 1./(err_srR*err_srR) ) )
                errSR = 1./math.sqrt( 1./(err_srL*err_srL)  +  1./(err_srR*err_srR) )
                errSR = errSR/sr
            if (srL>0 and srR<0):
                sr = srL
                errSR = err_srL/sr
            if (srL<0 and srR>0):
                sr = srR
                errSR = err_srR/sr
            if (ov<=1.5):
                errSRsyst = 0.2
            else:
                errSRsyst = 0.1
            errSR = math.sqrt(errSR*errSR+errSRsyst*errSRsyst) 
            if (sigma_tot>=sigma_noise(sr)):
                sigma_stoch_ref = math.sqrt(sigma_tot*sigma_tot - sigma_noise(sr)*sigma_noise(sr))
                err_sigma_noise = 0.5*(sigma_noise(sr*(1-errSR))-sigma_noise(sr*(1+errSR)))
                err_sigma_stoch_ref = 1./sigma_stoch_ref*math.sqrt( pow(err_sigma_tot*sigma_tot,2)+pow( sigma_noise(sr)*err_sigma_noise ,2) )
            else:
                print 'skipping bar%02d:  %.1f   %.1f'%(bar, sigma_tot,sigma_noise(sr))
                continue
                
        for i in range(0,g[sipm][bar].GetN()):
            sigma_meas = g[sipm][bar].GetY()[i]
            err_sigma_meas   = g[sipm][bar].GetErrorY(i)
            ov = g[sipm][bar].GetX()[i]
            if (ov not in Vovs[sipm]): continue

            Npe[sipm][ov]  = Npe_frac[sipm]*LO[sipm]*4.2*PDE(ov,sipm)/PDE(3.5,sipm)

            gain = Gain(ov, sipm) 
            g_psL = fPS[sipm][ov].Get('g_pulseShapeL_bar%02d_Vov%.2f'%(bar,ov))
            g_psR = fPS[sipm][ov].Get('g_pulseShapeR_bar%02d_Vov%.2f'%(bar,ov))
            if (g_psL!=None): g_psL.SetName('g_pulseShapeL_bar%02d_Vov%.2f_%s'%(bar,ov,sipm))
            if (g_psR!=None): g_psR.SetName('g_pulseShapeR_bar%02d_Vov%.2f_%s'%(bar,ov,sipm))
            timingThreshold = findTimingThreshold(f.Get('g_deltaT_totRatioCorr_vs_th_bar%02d_Vov%.2f_enBin01'%(bar,ov)),ov)
            srL = -1
            srR = -1
            sr = -1
            err_srL = -1
            err_srR = -1
            c = ROOT.TCanvas('c_%s'%(g_psL.GetName().replace('g_pulseShapeL','pulseShape')),'',600,600)  
            #hdummy = ROOT.TH2F('hdummy','', 100, min(g_psL.GetX())-1., 30., 100, 0., 15.)
            hdummy = ROOT.TH2F('hdummy','', 100, min(g_psL.GetX())-1., 5., 100, 0., 15.)
            hdummy.GetXaxis().SetTitle('time [ns]')
            hdummy.GetYaxis().SetTitle('amplitude [#muA]')
            hdummy.Draw()
            gtempL = ROOT.TGraphErrors()
            gtempR = ROOT.TGraphErrors()
            if (ov == 1.5):
#                print 'sono nella condizone ov: ', ov
                np = 1
            else:
                np = 3
            if (g_psL!=None): srL,err_srL = getSlewRateFromPulseShape(g_psL, timingThreshold, np, gtempL, c)
            if (g_psR!=None): srR,err_srR = getSlewRateFromPulseShape(g_psR, timingThreshold, np, gtempR, c) 
            line = ROOT.TLine(min(g_psL.GetX())-1., timingThreshold*0.313, 30., timingThreshold*0.313)
            line.SetLineStyle(7)
            line.SetLineWidth(2)
            line.SetLineColor(ROOT.kOrange+1)        
            line.Draw('same')
            c.SaveAs(outdir+'/plotsSR/'+c.GetName()+'.png')   
            hdummy.Delete()
            if (srL>0 and srR>0):
                # weighted average
                sr =  ( (srL/(err_srL*err_srL) + srR/(err_srR*err_srR) ) / (1./(err_srL*err_srL) + 1./(err_srR*err_srR) ) )
                errSR = 1./math.sqrt( 1./(err_srL*err_srL)  +  1./(err_srR*err_srR) )
            if (srL>0 and srR<0):
                sr = srL
                errSR = err_srL
            if (srL<0 and srR>0):
                sr = srR
                errSR = err_srR
            if (srL<0 and srR<0): continue
            if (ov<=1.5):
                errSRsyst = 0.2
            else:
                errSRsyst = 0.1
            errSR = math.sqrt(errSR*errSR+errSRsyst*errSRsyst*sr*sr) 
            #print ov, gain, Npe, srL, srR, sr, errSR

            g_Npe_vs_Vov[sipm].SetPoint(g_Npe_vs_Vov[sipm].GetN(), ov, Npe[sipm][ov])
            
            g_SR_vs_Vov[sipm][bar].SetPoint( g_SR_vs_Vov[sipm][bar].GetN(), ov, sr )
            g_SR_vs_Vov[sipm][bar].SetPointError( g_SR_vs_Vov[sipm][bar].GetN()-1, 0, errSR )
            g_SR_vs_GainNpe[sipm][bar].SetPoint( g_SR_vs_GainNpe[sipm][bar].GetN(), gain*Npe[sipm][ov], sr )
            g_SR_vs_GainNpe[sipm][bar].SetPointError( g_SR_vs_GainNpe[sipm][bar].GetN()-1, 0, errSR )
            g_bestTh_vs_Vov[sipm][bar].SetPoint( g_bestTh_vs_Vov[sipm][bar].GetN(), ov, timingThreshold )
            g_bestTh_vs_Vov[sipm][bar].SetPointError( g_bestTh_vs_Vov[sipm][bar].GetN()-1, 0, 0 )
            g_SR_vs_bar[sipm][ov].SetPoint( g_SR_vs_bar[sipm][ov].GetN(), bar, sr )
            g_SR_vs_bar[sipm][ov].SetPointError( g_SR_vs_bar[sipm][ov].GetN()-1, 0, errSR )
            g_bestTh_vs_bar[sipm][ov].SetPoint( g_bestTh_vs_bar[sipm][ov].GetN(), bar, timingThreshold )
            g_bestTh_vs_bar[sipm][ov].SetPointError( g_bestTh_vs_bar[sipm][ov].GetN()-1, 0, 0)


            g_Tot_vs_bar[sipm][ov].SetPoint(g_Tot_vs_bar[sipm][ov].GetN(), bar, g[sipm][bar].Eval(ov))
#            g_Tot_vs_bar[sipm][ov].SetPointError(g_Tot_vs_bar[sipm][ov].GetN()-1, 0, boh)

            
            g_Noise_vs_bar[sipm][ov].SetPoint( g_Noise_vs_bar[sipm][ov].GetN(), bar, sigma_noise(sr) )
            g_Noise_vs_bar[sipm][ov].SetPointError( g_Noise_vs_bar[sipm][ov].GetN()-1, 0,  0.5*(sigma_noise(sr*(1-errSR/sr))-sigma_noise(sr*(1+errSR/sr))) )
            g_Noise_vs_Vov[sipm][bar].SetPoint(g_Noise_vs_Vov[sipm][bar].GetN(), ov, sigma_noise(sr))
            g_Noise_vs_Vov[sipm][bar].SetPointError(g_Noise_vs_Vov[sipm][bar].GetN()-1, 0, 0.5*(sigma_noise(sr*(1-errSR/sr))-sigma_noise(sr*(1+errSR/sr))))
            # compute s_stoch as diff in quadrature between measured tRes and noise term
            if ( sigma_meas > sigma_noise(sr) ):
                s = math.sqrt(sigma_meas*sigma_meas-sigma_noise(sr)*sigma_noise(sr))
                es = 1./s * math.sqrt( pow(sigma_meas*g[sipm][bar].GetErrorY(i),2) + pow( sigma_noise(sr)*g_Noise_vs_Vov[sipm][bar].GetErrorY(g_Noise_vs_Vov[sipm][bar].GetN()-1),2) )
                g_Stoch_vs_Npe[sipm][bar].SetPoint(g_Stoch_vs_Npe[sipm][bar].GetN(), Npe[sipm][ov], s)
                g_Stoch_vs_Npe[sipm][bar].SetPointError(g_Stoch_vs_Npe[sipm][bar].GetN()-1, 0., es )

                g_StochMeas_vs_Vov[sipm][bar].SetPoint(g_StochMeas_vs_Vov[sipm][bar].GetN(), ov, s)
                g_StochMeas_vs_Vov[sipm][bar].SetPointError(g_StochMeas_vs_Vov[sipm][bar].GetN()-1, 0, es)
                g_StochMeas_vs_bar[sipm][ov].SetPoint( g_StochMeas_vs_bar[sipm][ov].GetN(), bar, s )
                g_StochMeas_vs_bar[sipm][ov].SetPointError( g_StochMeas_vs_bar[sipm][ov].GetN()-1, 0,  es)
                


            # compute stoch by scaling from 3.5 V OV
            sigma_stoch = sigma_stoch_ref/math.sqrt(  PDE(ov,sipm)/PDE(ov_ref,sipm)  )
            err_sigma_stoch = err_sigma_stoch_ref/math.sqrt( PDE(ov,sipm)/PDE(ov_ref,sipm) )
            g_Stoch_vs_Vov[sipm][bar].SetPoint(g_Stoch_vs_Vov[sipm][bar].GetN(), ov, sigma_stoch)
            g_Stoch_vs_Vov[sipm][bar].SetPointError(g_Stoch_vs_Vov[sipm][bar].GetN()-1, 0, err_sigma_stoch)
            g_Stoch_vs_bar[sipm][ov].SetPoint( g_Stoch_vs_bar[sipm][ov].GetN(), bar, sigma_stoch )
            g_Stoch_vs_bar[sipm][ov].SetPointError( g_Stoch_vs_bar[sipm][ov].GetN()-1, 0,  err_sigma_stoch)

            # tot resolution summing noise + stochastic in quadrature
            sigma_tot = math.sqrt( sigma_stoch*sigma_stoch + sigma_noise(sr)*sigma_noise(sr) )
            err_sigma_tot = 1./sigma_tot * math.sqrt( pow( err_sigma_stoch*sigma_stoch,2) + pow(sigma_noise(sr)*g_Noise_vs_Vov[sipm][bar].GetErrorY(g_Noise_vs_Vov[sipm][bar].GetN()-1),2))
            g_Tot_vs_Vov[sipm][bar].SetPoint(g_Tot_vs_Vov[sipm][bar].GetN(), ov, sigma_tot)
            g_Tot_vs_Vov[sipm][bar].SetPointError(g_Tot_vs_Vov[sipm][bar].GetN()-1, 0, err_sigma_tot)

            # tRes vs SR
            g_Stoch_vs_SR[sipm][ov].SetPoint(g_Stoch_vs_SR[sipm][ov].GetN(), sr, sigma_stoch)
            g_Stoch_vs_SR[sipm][ov].SetPointError(g_Stoch_vs_SR[sipm][ov].GetN()-1, errSR, err_sigma_stoch)

            g_Tot_vs_SR[sipm][ov].SetPoint(g_Tot_vs_SR[sipm][ov].GetN(), sr, sigma_meas)
            g_Tot_vs_SR[sipm][ov].SetPointError(g_Tot_vs_SR[sipm][ov].GetN()-1, errSR, err_sigma_meas)







#=======================================================================================================================
#--------------------------SR average over bars-------------------------------------------
fitAve_SR = {}
g_SRave_vs_Vov = {}

for sipm in sipmTypes:
    fitAve_SR[sipm] = {}
    g_SRave_vs_Vov[sipm] = ROOT.TGraphErrors()
    for ov in Vovs[sipm]:
        if (ov not in g_Tot_vs_SR[sipm].keys()): continue
        fitAve_SR[sipm][ov] = ROOT.TF1('fitAve_SR_sipm%s_Vov%s'%(sipm,ov),'pol0',0,16)
        fitAve_SR[sipm][ov].SetLineColor(cols[sipm])
        g_SR_vs_bar[sipm][ov].Fit(fitAve_SR[sipm][ov],'Q')
        g_SRave_vs_Vov[sipm].SetPoint(g_SRave_vs_Vov[sipm].GetN(), ov, fitAve_SR[sipm][ov].GetParameter(0))
        g_SRave_vs_Vov[sipm].SetPointError(g_SRave_vs_Vov[sipm].GetN()-1, 0, g_SR_vs_bar[sipm][ov].GetRMS(2))  #in prima approx, errore dato da rms su asse y

#---contributions to time resolution - average over bars
fitAve_Tot = {}
fitAve_Noise = {}
fitAve_Stoch = {}
fitAve_StochMeas = {}

g_TotAve_vs_Vov = {}
g_NoiseAve_vs_Vov = {}
g_StochAve_vs_Vov = {}
g_StochMeasAve_vs_Vov = {}

for sipm in sipmTypes:
    fitAve_Tot[sipm] = {}
    fitAve_Noise[sipm] = {}
    fitAve_Stoch[sipm] = {}
    fitAve_StochMeas[sipm] = {}

    g_TotAve_vs_Vov[sipm] = ROOT.TGraphErrors() 
    g_NoiseAve_vs_Vov[sipm] = ROOT.TGraphErrors()
    g_StochAve_vs_Vov[sipm] = ROOT.TGraphErrors()
    g_StochMeasAve_vs_Vov[sipm] = ROOT.TGraphErrors()



    for ov in Vovs[sipm]:
        if (ov not in g_Tot_vs_SR[sipm].keys()): continue 
        fitAve_Tot[sipm][ov] = ROOT.TF1('fitAve_Tot_sipm%s_Vov%s'%(sipm,ov),'pol0',0,16)
        fitAve_Noise[sipm][ov] = ROOT.TF1('fitAve_Noise_sipm%s_Vov%s'%(sipm,ov),'pol0',0,16)
        fitAve_Stoch[sipm][ov] = ROOT.TF1('fitAve_Stoch_sipm%s_Vov%s'%(sipm,ov),'pol0',0,16)
        fitAve_StochMeas[sipm][ov] = ROOT.TF1('fitAve_StochMeas_sipm%s_Vov%s'%(sipm,ov),'pol0',0,16)

        g_Tot_vs_bar[sipm][ov].Fit(fitAve_Tot[sipm][ov])
        g_Noise_vs_bar[sipm][ov].Fit(fitAve_Noise[sipm][ov])
        g_Stoch_vs_bar[sipm][ov].Fit(fitAve_Stoch[sipm][ov])  
        g_StochMeas_vs_bar[sipm][ov].Fit(fitAve_StochMeas[sipm][ov])  

        g_TotAve_vs_Vov[sipm].SetPoint(g_TotAve_vs_Vov[sipm].GetN(), ov, fitAve_Tot[sipm][ov].GetParameter(0))
        g_TotAve_vs_Vov[sipm].SetPointError(g_TotAve_vs_Vov[sipm].GetN()-1, 0,  g_Tot_vs_bar[sipm][ov].GetRMS(2)/(math.sqrt(g_Tot_vs_bar[sipm][ov].GetN())))

        g_NoiseAve_vs_Vov[sipm].SetPoint(g_NoiseAve_vs_Vov[sipm].GetN(), ov, fitAve_Noise[sipm][ov].GetParameter(0))
        g_NoiseAve_vs_Vov[sipm].SetPointError(g_NoiseAve_vs_Vov[sipm].GetN()-1, 0,  g_Noise_vs_bar[sipm][ov].GetRMS(2)/(math.sqrt(g_Noise_vs_bar[sipm][ov].GetN())))

        g_StochAve_vs_Vov[sipm].SetPoint(g_StochAve_vs_Vov[sipm].GetN(), ov, fitAve_Stoch[sipm][ov].GetParameter(0))
        g_StochAve_vs_Vov[sipm].SetPointError(g_StochAve_vs_Vov[sipm].GetN()-1, 0,  g_Stoch_vs_bar[sipm][ov].GetRMS(2)/(math.sqrt(g_Stoch_vs_bar[sipm][ov].GetN())))



        g_StochMeasAve_vs_Vov[sipm].SetPoint(g_StochMeasAve_vs_Vov[sipm].GetN(), ov, fitAve_StochMeas[sipm][ov].GetParameter(0))
        g_StochMeasAve_vs_Vov[sipm].SetPointError(g_StochMeasAve_vs_Vov[sipm].GetN()-1, 0,  g_StochMeas_vs_bar[sipm][ov].GetRMS(2)/(math.sqrt(g_StochMeas_vs_bar[sipm][ov].GetN())))

#=======================================================================================================================











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
    print sipmTypes[0], sipmTypes[2],' ratio stochastic term at 3.5 V OV = ', ratio_stoch
    g_ratio_stoch3.SetPoint(g_ratio_stoch3.GetN(), bar, ratio_stoch)
    g_ratio_stoch3.SetPointError(g_ratio_stoch3.GetN()-1, 0, err_ratio_stoch)
        







########################################################################
#----------disegno tutto-----------


# draw
c1 = {}
c2 = {}
c3 = {}
c4 = {}
hdummy1 = {}
hdummy2 = {}
hdummy3 = {}
hdummy4 = {}
leg = {}

h = {}
for sipm in sipmTypes:
    c1[sipm] = {}
    hdummy1[sipm] = {}
    c2[sipm] = {}
    hdummy2[sipm] = {}
    h[sipm] = ROOT.TH1F('h_coeff_%s'%sipm,'',100,-2.0,1.0)
    leg[sipm] = ROOT.TLegend(0.55,0.70,0.89,0.89)
    leg[sipm].SetBorderSize(0)
    for i,bar in enumerate(bars[sipm]):
        c1[sipm][bar] =  ROOT.TCanvas('c_timeResolution_vs_Vov_bar%02d_%s'%(bar,sipm),'c_timeResolution_vs_Vov_bar%02d_%s'%(bar,sipm),600,600)
        c1[sipm][bar].SetGridy()
        c1[sipm][bar].cd()
        hdummy1[sipm][bar] = ROOT.TH2F('hdummy1_%s_%d'%(sipm,bar),'',100,0,8,100,0,100)
        hdummy1[sipm][bar].GetXaxis().SetTitle('V_{OV} [V]')
        hdummy1[sipm][bar].GetYaxis().SetTitle('#sigma_{t} [ps]')
        hdummy1[sipm][bar].Draw()
        g[sipm][bar].SetMarkerStyle(20)
        g[sipm][bar].SetMarkerSize(1)
        g[sipm][bar].SetMarkerColor(1)
        g[sipm][bar].SetLineColor(1)
        g[sipm][bar].SetLineWidth(2)
        g[sipm][bar].Draw('psame')
        outfile[sipm].cd()
        g[sipm][bar].Write('g_timeResolution_vs_Vov_bar%02d'%(bar))

        g_Noise_vs_Vov[sipm][bar].SetLineWidth(2)
        g_Noise_vs_Vov[sipm][bar].SetLineColor(ROOT.kBlue)
        g_Noise_vs_Vov[sipm][bar].SetFillColor(ROOT.kBlue)
        g_Noise_vs_Vov[sipm][bar].SetFillColorAlpha(ROOT.kBlue,0.5)
        g_Noise_vs_Vov[sipm][bar].SetFillStyle(3004)
        g_Noise_vs_Vov[sipm][bar].Draw('E3lsame')
        outfile[sipm].cd() 
        g_Noise_vs_Vov[sipm][bar].Write('g_Noise_vs_Vov_bar%02d'%(bar))

        g_Stoch_vs_Vov[sipm][bar].SetLineWidth(2)
        g_Stoch_vs_Vov[sipm][bar].SetLineColor(ROOT.kGreen+2)
        g_Stoch_vs_Vov[sipm][bar].SetFillColor(ROOT.kGreen+2)
        g_Stoch_vs_Vov[sipm][bar].SetFillStyle(3001)
        g_Stoch_vs_Vov[sipm][bar].SetFillColorAlpha(ROOT.kGreen+2,0.5)
        g_Stoch_vs_Vov[sipm][bar].Draw('E3lsame')
        outfile[sipm].cd() 

        g_Stoch_vs_Vov[sipm][bar].Write('g_Stoch_vs_Vov_bar%02d'%(bar))
        g_StochMeas_vs_Vov[sipm][bar].Write('g_StochMeas_vs_Vov_bar%02d'%(bar))

        g_Tot_vs_Vov[sipm][bar].SetLineWidth(2)
        g_Tot_vs_Vov[sipm][bar].SetLineColor(ROOT.kRed+1)
        g_Tot_vs_Vov[sipm][bar].SetFillColor(ROOT.kRed+1)
        g_Tot_vs_Vov[sipm][bar].SetFillColorAlpha(ROOT.kRed+1,0.5)
        g_Tot_vs_Vov[sipm][bar].SetFillStyle(3001)
#        g_Tot_vs_Vov[sipm][bar].Draw('E3lsame')
        outfile[sipm].cd() 
        g_Tot_vs_Vov[sipm][bar].Write('g_timeResolutionExpected_vs_Vov_bar%02d'%(bar))

        if (i==0):
            leg[sipm].AddEntry(g[sipm][bar], 'data', 'PL')
            leg[sipm].AddEntry(g_Noise_vs_Vov[sipm][bar], 'noise', 'PL')
            leg[sipm].AddEntry(g_Stoch_vs_Vov[sipm][bar], 'stoch', 'PL')
            leg[sipm].AddEntry(g_Tot_vs_Vov[sipm][bar], 'stoch #oplus noise', 'PL')
        leg[sipm].Draw('same')
        latex = ROOT.TLatex(0.15,0.83,'%s'%(sipm.replace('_nonIrr_','+')))
        latex.SetNDC()
        latex.SetTextSize(0.035)
        latex.SetTextFont(42)
        latex.Draw('same')
        c1[sipm][bar].SaveAs(outdir+'/'+c1[sipm][bar].GetName()+'.png')
        c1[sipm][bar].SaveAs(outdir+'/'+c1[sipm][bar].GetName()+'.pdf')

        # vs npe
        c2[sipm][bar] =  ROOT.TCanvas('c_timeResolution_vs_Npe_bar%02d_%s'%(bar,sipm),'c_timeResolution_vs_Npe_bar%02d_%s'%(bar,sipm),600,600)
        c2[sipm][bar].SetGridy()
        c2[sipm][bar].cd()
        hdummy2[sipm][bar] = ROOT.TH2F('hdummy2_%s_%d'%(sipm,bar),'',10000,1000,10000,100,0,100)
        hdummy2[sipm][bar].GetXaxis().SetTitle('Npe')
        hdummy2[sipm][bar].GetYaxis().SetTitle('#sigma_{t} [ps]')
        hdummy2[sipm][bar].Draw()
        g_Stoch_vs_Npe[sipm][bar].SetMarkerStyle(20)
        g_Stoch_vs_Npe[sipm][bar].SetMarkerSize(0.8)
        g_Stoch_vs_Npe[sipm][bar].SetMarkerColor(ROOT.kGreen+2)
        g_Stoch_vs_Npe[sipm][bar].SetLineWidth(1)
        g_Stoch_vs_Npe[sipm][bar].SetLineColor(ROOT.kGreen+2)
        g_Stoch_vs_Npe[sipm][bar].Draw('psame')
        fitFun = ROOT.TF1('fitFun_%s_%.2d'%(sipm,bar),'[0]*pow(x,[1])',2000,9500)
        fitFun.SetParameters(30,-0.5)
        fitFun.SetLineColor(ROOT.kGreen+3)
        g_Stoch_vs_Npe[sipm][bar].Fit(fitFun,'QRS+')
        if (fitFun.GetNDF()>0): h[sipm].Fill(fitFun.GetParameter(1))

        outfile[sipm].cd() 
        g_Stoch_vs_Npe[sipm][bar].Write('g_Stoch_vs_Npe_bar%02d'%(bar))

        c2[sipm][bar].SaveAs(outdir+'/'+c2[sipm][bar].GetName()+'.png')
        c2[sipm][bar].SaveAs(outdir+'/'+c2[sipm][bar].GetName()+'.pdf')

    ROOT.gStyle.SetOptStat(1111)
    cc =  ROOT.TCanvas('c_coeff_%s'%(sipm),'c_coeff_%s'%(sipm),600,600)
    h[sipm].GetXaxis().SetTitle('#alpha')
    h[sipm].Draw('')
    cc.SaveAs(outdir+'/'+cc.GetName()+'_noRedLine.png')
    ROOT.gStyle.SetOptStat(0)
    #cc.Delete()


# total time resolution vs SR
for sipm in sipmTypes:
    for ov in Vovs[sipm]:
        if (ov not in g_Tot_vs_SR[sipm].keys()): continue
        c =  ROOT.TCanvas('c_timeResolution_vs_SR_%s_Vov%.2f'%(sipm,ov),'c_timeResolution_vs_SR_%s_Vov%.2f'%(sipm,ov),600,600)
        c.SetGridy()
        c.cd()
        xmin = 0.
        xmax = g_Tot_vs_SR[sipm][ov].GetMean() + 5.
        ymin = g_Tot_vs_SR[sipm][ov].GetMean(2)-20.
        ymax = g_Tot_vs_SR[sipm][ov].GetMean(2)+20.
        hdummy = ROOT.TH2F('hdummy_%s_%d'%(sipm,ov),'',100, xmin, xmax, 100, ymin, ymax)
        hdummy.GetXaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
        hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
        hdummy.Draw()
        g_Tot_vs_SR[sipm][ov].SetMarkerStyle(20)
        g_Tot_vs_SR[sipm][ov].SetMarkerSize(1)
        g_Tot_vs_SR[sipm][ov].SetMarkerColor(1)
        g_Tot_vs_SR[sipm][ov].SetLineColor(1)
        g_Tot_vs_SR[sipm][ov].SetLineWidth(2)
        g_Tot_vs_SR[sipm][ov].Draw('psame')

        outfile[sipm].cd() 
        g_Tot_vs_SR[sipm][ov].Write('g_timeResolution_vs_SR_Vov%.2f'%(ov))

        c.SaveAs(outdir+'/'+c.GetName()+'.png')
        c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
        hdummy.Delete()
        c.Delete()



# SR and best threshold vs Vov
leg2 = ROOT.TLegend(0.15,0.70,0.45,0.89)
leg2.SetBorderSize(0)
leg2.SetFillStyle(0)
for i,bar in enumerate(bars[sipm]):
    c3[bar] = ROOT.TCanvas('c_slewRate_vs_Vov_bar%02d'%(bar),'c_slewRate_vs_Vov_bar%02d'%(bar),600,600)
    c3[bar].SetGridy()
    c3[bar].cd()
    hdummy3[bar] = ROOT.TH2F('hdummy3_%d'%(bar),'',100,0,8,100,0,35)
    hdummy3[bar].GetXaxis().SetTitle('V_{OV} [V]')
    hdummy3[bar].GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
    hdummy3[bar].Draw()
    for j,sipm in enumerate(sipmTypes):
        if (i==0):
            leg2.AddEntry(g_SR_vs_Vov[sipm][bar], '%s'%sipm, 'PL')
        if (bar not in g_SR_vs_Vov[sipm].keys()):continue
        g_SR_vs_Vov[sipm][bar].SetMarkerStyle( markers[sipm] )
        g_SR_vs_Vov[sipm][bar].SetMarkerColor(cols[sipm])
        g_SR_vs_Vov[sipm][bar].SetLineColor(cols[sipm])
        g_SR_vs_Vov[sipm][bar].Draw('psame')

        outfile[sipm].cd() 
        g_SR_vs_Vov[sipm][bar].Write('g_slewRate_vs_Vov_bar%02d'%(bar))

    leg2.Draw()
    c3[bar].SaveAs(outdir+'/'+c3[bar].GetName()+'.png')
    c3[bar].SaveAs(outdir+'/'+c3[bar].GetName()+'.pdf')
    c3[bar].Delete()
    hdummy3[bar].Delete() 

    c3[bar] = ROOT.TCanvas('c_slewRate_vs_GainNpe_bar%02d'%(bar),'c_slewRate_vs_GainNpe_bar%02d'%(bar),600,600)
    c3[bar].SetGridy()
    c3[bar].cd()
    #hdummy3[bar] = ROOT.TH2F('hdummy3_%d'%(bar),'',100,0,2,100,0,35)
    hdummy3[bar] = ROOT.TH2F('hdummy3_%d'%(bar),'',100,0,3E09,100,0,35)
    hdummy3[bar].GetXaxis().SetTitle('gain x Npe')
    hdummy3[bar].GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
    hdummy3[bar].Draw()
    for j,sipm in enumerate(sipmTypes):
        if (bar not in g_SR_vs_GainNpe[sipm].keys()): continue
        g_SR_vs_GainNpe[sipm][bar].SetMarkerStyle( markers[sipm] )
        g_SR_vs_GainNpe[sipm][bar].SetMarkerColor(cols[sipm])
        g_SR_vs_GainNpe[sipm][bar].SetLineColor(cols[sipm])
        g_SR_vs_GainNpe[sipm][bar].Draw('psame')
        outfile[sipm].cd() 
        g_SR_vs_GainNpe[sipm][bar].Write('g_slewRate_vs_GainNpe_bar%02d'%(bar))


    leg2.Draw()
    c3[bar].SaveAs(outdir+'/'+c3[bar].GetName()+'.png')
    c3[bar].SaveAs(outdir+'/'+c3[bar].GetName()+'.pdf')
    
    c4[bar] = ROOT.TCanvas('c_bestTh_vs_Vov_bar%02d'%(bar),'c_bestTh_vs_Vov_bar%02d'%(bar),600,600)
    c4[bar].SetGridy()
    c4[bar].cd()
    hdummy4[bar] = ROOT.TH2F('hdummy4_%d'%(bar),'',100,0,8,100,0,20)
    hdummy4[bar].GetXaxis().SetTitle('V_{OV} [V]')
    hdummy4[bar].GetYaxis().SetTitle('best threshold [DAC]')
    hdummy4[bar].Draw()
    for j,sipm in enumerate(sipmTypes):
        if (bar not in g_bestTh_vs_Vov[sipm].keys()):continue
        g_bestTh_vs_Vov[sipm][bar].SetMarkerStyle( markers[sipm] )
        g_bestTh_vs_Vov[sipm][bar].SetMarkerColor(cols[sipm])
        g_bestTh_vs_Vov[sipm][bar].SetLineColor(cols[sipm])
        g_bestTh_vs_Vov[sipm][bar].Draw('plsame')
        
        outfile[sipm].cd() 
        g_bestTh_vs_Vov[sipm][bar].Write('g_bestTh_vs_Vov_bar%02d'%(bar))


    c4[bar].SaveAs(outdir+'/'+c4[bar].GetName()+'.png')
    c4[bar].SaveAs(outdir+'/'+c4[bar].GetName()+'.pdf')



    
# SR and best threshold vs bar
c5 = {}
hdummy5 = {}
c6 = {}
hdummy6 = {}
c7 = {}
hdummy7 = {}
c8 = {}
hdummy8 = {}
for sipm in sipmTypes:  
    for ov in Vovs[sipm]:
        ROOT.gStyle.SetOptStat(0)
        c5[ov] = ROOT.TCanvas('c_slewRate_vs_bar_Vov%.2f'%(ov),'c_slewRate_vs_bar_Vov%.2f'%(ov),600,600)
        c5[ov].SetGridy()
        c5[ov].cd()
        ymax = 35.
        if (ov == 1.50): ymax = 15.
        hdummy5[ov] = ROOT.TH2F('hdummy5_%d'%(ov),'',100,-0.5,15.5,100,0,ymax)
        hdummy5[ov].GetXaxis().SetTitle('bar')
        hdummy5[ov].GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
        hdummy5[ov].Draw()
        for j,sipm in enumerate(sipmTypes):
            if (ov not in g_SR_vs_bar[sipm].keys()): continue
            g_SR_vs_bar[sipm][ov].SetMarkerStyle( markers[sipm] )
            g_SR_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])
            g_SR_vs_bar[sipm][ov].SetLineColor(cols[sipm])
            g_SR_vs_bar[sipm][ov].Draw('psame')
            outfile[sipm].cd() 
            g_SR_vs_bar[sipm][ov].Write('g_slewRate_vs_bar_Vov%.2f'%(ov))

        leg2.Draw()
        latex = ROOT.TLatex(0.65,0.82,'V_{OV} = %.2f V'%ov)
        latex.SetNDC()
        latex.SetTextSize(0.035)
        latex.SetTextFont(42)
        latex.Draw('same')
        c5[ov].SaveAs(outdir+'/'+c5[ov].GetName()+'.png')
        c5[ov].SaveAs(outdir+'/'+c5[ov].GetName()+'.pdf')

        c6[ov] = ROOT.TCanvas('c_bestTh_vs_bar_Vov%.2f'%(ov),'c_bestTh_vs_bar_Vov%.2f'%(ov),600,600)
        c6[ov].SetGridy()
        c6[ov].cd()
        hdummy6[ov] = ROOT.TH2F('hdummy6_%d'%(ov),'',100,-0.5,15.5,100,0,20)
        hdummy6[ov].GetXaxis().SetTitle('bar')
        hdummy6[ov].GetYaxis().SetTitle('timing threshold [DAC]')
        hdummy6[ov].Draw()
        for j,sipm in enumerate(sipmTypes):
            if (ov not in g_bestTh_vs_bar[sipm].keys()): continue
            g_bestTh_vs_bar[sipm][ov].SetMarkerStyle( markers[sipm] )
            g_bestTh_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])
            g_bestTh_vs_bar[sipm][ov].SetLineColor(cols[sipm])
            g_bestTh_vs_bar[sipm][ov].Draw('plsame')
            outfile[sipm].cd() 
            g_bestTh_vs_bar[sipm][ov].Write('g_bestTh_vs_bar_Vov%.2f'%(ov))

        leg2.Draw()        
        c6[ov].SaveAs(outdir+'/'+c6[ov].GetName()+'.png')
        c6[ov].SaveAs(outdir+'/'+c6[ov].GetName()+'.pdf')

        c7[ov] = ROOT.TCanvas('c_noise_vs_bar_Vov%.2f'%(ov),'c_noise_vs_bar_Vov%.2f'%(ov),600,600)
        c7[ov].SetGridy()
        c7[ov].cd()
        hdummy7[ov] = ROOT.TH2F('hdummy7_%d'%(ov),'',100,-0.5,15.5,100,0,80)
        hdummy7[ov].GetXaxis().SetTitle('bar')
        hdummy7[ov].GetYaxis().SetTitle('#sigma_{t, noise} [ps]')
        hdummy7[ov].Draw()
        for j,sipm in enumerate(sipmTypes):
            if (ov not in g_Noise_vs_bar[sipm].keys()): continue
            g_Noise_vs_bar[sipm][ov].SetMarkerStyle( markers[sipm] )
            g_Noise_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])
            g_Noise_vs_bar[sipm][ov].SetLineColor(cols[sipm])
            g_Noise_vs_bar[sipm][ov].Draw('psame')
            outfile[sipm].cd() 
            g_Noise_vs_bar[sipm][ov].Write('g_Noise_vs_bar_Vov%.2f'%(ov))

        leg2.Draw()        
        latex = ROOT.TLatex(0.65,0.82,'V_{OV} = %.2f V'%ov)
        latex.SetNDC()
        latex.SetTextSize(0.035)
        latex.SetTextFont(42)
        latex.Draw('same')
        c7[ov].SaveAs(outdir+'/'+c7[ov].GetName()+'.png')
        c7[ov].SaveAs(outdir+'/'+c7[ov].GetName()+'.pdf')

        c8[ov] = ROOT.TCanvas('c_stoch_vs_bar_Vov%.2f'%(ov),'c_stoch_vs_bar_Vov%.2f'%(ov),600,600)
        c8[ov].SetGridy()
        c8[ov].cd()
        hdummy8[ov] = ROOT.TH2F('hdummy8_%d'%(ov),'',100,-0.5,15.5,100,0,80)
        hdummy8[ov].GetXaxis().SetTitle('bar')
        hdummy8[ov].GetYaxis().SetTitle('#sigma_{t, stoch} [ps]')
        hdummy8[ov].Draw()
        for j,sipm in enumerate(sipmTypes):
            if (ov not in g_Stoch_vs_bar[sipm].keys()): continue
            g_Stoch_vs_bar[sipm][ov].SetMarkerStyle( markers[sipm] )
            g_Stoch_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])
            g_Stoch_vs_bar[sipm][ov].SetLineColor(cols[sipm])
            g_Stoch_vs_bar[sipm][ov].Draw('psame')
            outfile[sipm].cd() 
            g_Stoch_vs_bar[sipm][ov].Write('g_Stoch_vs_bar_Vov%.2f'%(ov))
            g_StochMeas_vs_bar[sipm][ov].Write('g_StochMeas_vs_bar_Vov%.2f'%(ov))

        leg2.Draw()        
        c8[ov].SaveAs(outdir+'/'+c8[ov].GetName()+'.png')
        c8[ov].SaveAs(outdir+'/'+c8[ov].GetName()+'.pdf')
    
# ratio of photo-stat. terms:
for i,g in enumerate([g_ratio_stoch1, g_ratio_stoch2, g_ratio_stoch3]):
    if i == 0:
        sipm1 = sipmTypes[1]
        sipm2 = sipmTypes[0]
    if i == 1:
        sipm1 = sipmTypes[1]
        sipm2 = sipmTypes[2]
    if i == 2:
        sipm1 = sipmTypes[0]
        sipm2 = sipmTypes[2]
    
    cc = ROOT.TCanvas('c_ratioStoch_vs_bar_%s_%s'%(sipm1, sipm2),'c_ratioStoch_vs_bar_%s_%s_'%(sipm1, sipm2),600,600)
    print cc.GetName()
    cc.cd()
    hdummy = ROOT.TH2F('hdummy','',16,-0.5,15.5,100,0.2,1.5)
    hdummy.GetXaxis().SetTitle('bar')
    hdummy.GetYaxis().SetTitle('#sigma_{stoch.}^{%s}/#sigma_{stoch.}^{%s}'%(labels[sipm1],labels[sipm2]))
    hdummy.Draw('')
    g.SetMarkerStyle(20)
    g.Draw('psame')
    expRatioLO    = math.sqrt(Npe[sipm2][ov_ref]/Npe[sipm1][ov_ref])
    expRatioLOTau = math.sqrt((Npe[sipm2][ov_ref]/tau[sipm2])/(Npe[sipm1][ov_ref]/tau[sipm1]))
    #expRatioLO    = math.sqrt(LO[sipm2]/LO[sipm1])
    #expRatioLOTau = math.sqrt((LO[sipm2]/tau[sipm2])/(LO[sipm1]/tau[sipm1]))
    ll = ROOT.TLine(0, expRatioLO, 15, expRatioLO)
    ll.SetLineStyle(7)
    ll.SetLineWidth(2)
    ll.SetLineColor(ROOT.kGray+1)
    ll.Draw('same')
    lll = ROOT.TLine(0, expRatioLOTau, 15, expRatioLOTau)
    lll.SetLineStyle(7)
    lll.SetLineWidth(2)
    lll.SetLineColor(ROOT.kBlue)
    lll.Draw('same')
    leg2 = ROOT.TLegend(0.15,0.15,0.55,0.35)
    leg2.SetBorderSize(0)
    leg2.AddEntry(g,'ratio of photostat. terms','PL')
    leg2.AddEntry(ll,'sqrt(LO) = %.2f'%expRatioLO,'L')
    leg2.AddEntry(lll,'sqrt(LO/#tau) = %.2f'%expRatioLOTau,'L')
    leg2.Draw('same')
    fitFun=ROOT.TF1('fitFun','pol0',0,16)
    fitFun.SetLineColor(1)
    g.Fit(fitFun,'QRS')
    hint = ROOT.TH1F("hint","Fitted Gaussian with .95 conf.band", 16, -0.5, 15.5)
    hint.SetMarkerStyle(1)
    hint.SetMarkerSize(0)
    tvf = ROOT.TVirtualFitter.GetFitter()
    tvf.GetConfidenceIntervals(hint)
    hint.SetFillColorAlpha(1,0.2)
    hint.Draw("e3 same")

    
    print 'ratio of stoch. terms expected from sqrt(LO)      = ', expRatioLO
    print 'ratio of stoch. terms expected from sqrt(LO/tau)  = ', expRatioLOTau
    print 'ratio of stoch. terms measured at 3.5 V           = ', fitFun.GetParameter(0)
    cc.SaveAs(outdir+'/'+cc.GetName()+'.png')                        
    cc.SaveAs(outdir+'/'+cc.GetName()+'.pdf')                        
    hdummy.Delete()

for sipm in sipmTypes: 
    for ov in Vovs[sipm]:
            print sipm, ov, '  average stoch. term = ', g_Stoch_vs_bar[sipm][ov].GetMean(2),' ps' 
            print sipm, ov, '  average noise  term = ', g_Noise_vs_bar[sipm][ov].GetMean(2),' ps'
    






#=======================================================================================
#------Npe vs Vov------
c_Npe = {}
hdummy_Npe_Vov = {}

leg_Npe_Vov = ROOT.TLegend(0.15,0.70,0.45,0.89)
leg_Npe_Vov.SetBorderSize(0)
leg_Npe_Vov.SetFillStyle(0)

c_Npe_vs_Vov = ROOT.TCanvas('c_Npe_vs_Vov','c_Npe_vs_Vov',600,600)
c_Npe_vs_Vov.SetGridy()
c_Npe_vs_Vov.cd()
hdummy_Npe_Vov = ROOT.TH2F('hdummy_Npe_Vov','',100,0,8,100,0,9000)
hdummy_Npe_Vov.GetXaxis().SetTitle('V_{OV} [V]')
hdummy_Npe_Vov.GetYaxis().SetTitle('N_{pe} [p.e./MeV]')
hdummy_Npe_Vov.Draw()

for j, sipm, in enumerate(sipmTypes):
    leg_Npe_Vov.AddEntry(g_Npe_vs_Vov[sipm], '%s'%sipm, 'PL')
    
    g_Npe_vs_Vov[sipm].SetMarkerStyle( markers[sipm] )
    g_Npe_vs_Vov[sipm].SetMarkerColor(cols[sipm])
    g_Npe_vs_Vov[sipm].SetLineColor(cols[sipm])
    g_Npe_vs_Vov[sipm].Draw('psame')

    outfile[sipm].cd() 
    g_Npe_vs_Vov[sipm].Write('g_Npe_vs_Vov')

leg_Npe_Vov.Draw()
c_Npe_vs_Vov.SaveAs(outdir+'/'+c_Npe_vs_Vov.GetName()+'.png')
hdummy_Npe_Vov.Delete()



#------SRave vs Vov------
c_SRave = {}
hdummy_SRave = {}

leg_SRave_Vov = ROOT.TLegend(0.15,0.70,0.45,0.89)
leg_SRave_Vov.SetBorderSize(0)
leg_SRave_Vov.SetFillStyle(0)

c_SRave_vs_Vov = ROOT.TCanvas('c_slewRateAve_vs_Vov','c_slewRateAve_vs_Vov',600,600)
c_SRave_vs_Vov.SetGridy()
c_SRave_vs_Vov.cd()
hdummy_SRave_Vov = ROOT.TH2F('hdummy_SRave_Vov','',100,0,8,100,0,35)
hdummy_SRave_Vov.GetXaxis().SetTitle('V_{OV} [V]')
hdummy_SRave_Vov.GetYaxis().SetTitle('slew rate^{ave} at the timing thr. [#muA/ns]')
hdummy_SRave_Vov.Draw()

for j, sipm, in enumerate(sipmTypes):
    leg_SRave_Vov.AddEntry(g_SRave_vs_Vov[sipm], '%s'%sipm, 'PL')
    
    g_SRave_vs_Vov[sipm].SetMarkerStyle( markers[sipm] )
    g_SRave_vs_Vov[sipm].SetMarkerColor(cols[sipm])
    g_SRave_vs_Vov[sipm].SetLineColor(cols[sipm])
    g_SRave_vs_Vov[sipm].Draw('psame')

    outfile[sipm].cd() 
    g_SRave_vs_Vov[sipm].Write('g_slewRate_vs_Vov')

leg_SRave_Vov.Draw()
c_SRave_vs_Vov.SaveAs(outdir+'/'+c_SRave_vs_Vov.GetName()+'.png')
hdummy_SRave_Vov.Delete()


#----canvas - average of Tot, Noise, Stoch vs Vov-----

c_ave = {}
hdummy_ave = {}
leg_ave = {}

for sipm in sipmTypes:
    leg_ave[sipm] = ROOT.TLegend(0.55,0.70,0.89,0.89)
    leg_ave[sipm].SetBorderSize(0)

    c_ave[sipm] = ROOT.TCanvas('c_timeResolutionAve_vs_Vov_%s'%sipm,'c_timeResolutionAve_vs_Vov_%s'%sipm,600,600)
    c_ave[sipm].SetGridy()
    c_ave[sipm].cd()
    
    hdummy_ave[sipm] = ROOT.TH2F('hdummy_ave_%s'%(sipm),'',100,0,8,100,0,100)
    hdummy_ave[sipm].GetXaxis().SetTitle('V_{OV} [V]')
    hdummy_ave[sipm].GetYaxis().SetTitle('#sigma_{t} [ps]')
    hdummy_ave[sipm].Draw()
    
    g_TotAve_vs_Vov[sipm].SetMarkerStyle(20)
    g_TotAve_vs_Vov[sipm].SetMarkerSize(1)
    g_TotAve_vs_Vov[sipm].SetMarkerColor(1)
    g_TotAve_vs_Vov[sipm].SetLineColor(1)
    g_TotAve_vs_Vov[sipm].SetLineWidth(2)
    g_TotAve_vs_Vov[sipm].Draw('plsame')
    outfile[sipm].cd()
    g_TotAve_vs_Vov[sipm].Write('g_timeResolutionAve_vs_Vov')

    g_NoiseAve_vs_Vov[sipm].SetLineColor(ROOT.kBlue)
    g_NoiseAve_vs_Vov[sipm].SetFillColor(ROOT.kBlue)
    g_NoiseAve_vs_Vov[sipm].SetFillColorAlpha(ROOT.kBlue,0.5)
    g_NoiseAve_vs_Vov[sipm].SetFillStyle(3004)
    g_NoiseAve_vs_Vov[sipm].SetLineWidth(2)
    g_NoiseAve_vs_Vov[sipm].Draw('E3lsame')
    outfile[sipm].cd()
    g_NoiseAve_vs_Vov[sipm].Write('g_NoiseAve_vs_Vov')

    g_StochAve_vs_Vov[sipm].SetLineColor(ROOT.kGreen+2)
    g_StochAve_vs_Vov[sipm].SetFillColor(ROOT.kGreen+2)
    g_StochAve_vs_Vov[sipm].SetFillColorAlpha(ROOT.kGreen+2,0.5)
    g_StochAve_vs_Vov[sipm].SetFillStyle(3001)
    g_StochAve_vs_Vov[sipm].SetLineWidth(2)
    g_StochAve_vs_Vov[sipm].Draw('E3lsame')
    outfile[sipm].cd()
    g_StochAve_vs_Vov[sipm].Write('g_StochAve_vs_Vov')
    g_StochMeasAve_vs_Vov[sipm].Write('g_StochMeasAve_vs_Vov')

    leg_ave[sipm].AddEntry(g_TotAve_vs_Vov[sipm], 'data', 'PL')
    leg_ave[sipm].AddEntry(g_NoiseAve_vs_Vov[sipm], 'noise', 'PL')
    leg_ave[sipm].AddEntry(g_StochAve_vs_Vov[sipm], 'stoch', 'PL')
    leg_ave[sipm].Draw('same')

    latex = ROOT.TLatex(0.15,0.83,'%s'%(sipm.replace('_nonIrr_','+')))
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextFont(42)
    latex.Draw('same')

    c_ave[sipm].SaveAs(outdir+'/'+c_ave[sipm].GetName()+'.png')


#=======================================================================================


raw_input('OK?')
