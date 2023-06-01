#! /usr/bin/env python
import math
import array
import sys

import ROOT



def getSlewRateFromPulseShape(g1, timingThreshold, npoints, gtemp, canvas=None):
    if ( g1.GetN() < npoints): return (-1, -1)

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

        # if (ov<=1.5 and x > 5): continue

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
   #fitXMin = h1_deltaT.GetMean() - 3*h1_deltaT.GetRMS()
   #fitXMax = h1_deltaT.GetMean() + 3*h1_deltaT.GetRMS()
   fitFunc.SetRange(fitXMin, fitXMax)
   h1_deltaT.Fit('fitFunc','QNRL','', fitXMin, fitXMax)
   #fitFunc.SetRange(fitFunc.GetParameter(1) - 3.0*fitFunc.GetParameter(2), fitFunc.GetParameter(1) + 3.0*fitFunc.GetParameter(2))
   fitFunc.SetRange(fitFunc.GetParameter(1) - 1.0*fitFunc.GetParameter(2), fitFunc.GetParameter(1) + 1.0*fitFunc.GetParameter(2))
   h1_deltaT.Fit('fitFunc','QNRL')
   fitFunc.SetRange(fitFunc.GetParameter(1) - 2.5*fitFunc.GetParameter(2), fitFunc.GetParameter(1) + 2.5*fitFunc.GetParameter(2))
   h1_deltaT.Fit('fitFunc','QRSL+')

   #if (fitFunc==None): continue                    
   #if (fitFunc.GetParameter(2) > 1000): continue
   #if (fitFunc.GetParameter(2) < 20): continue
   #if (fitFunc.GetParError(2) > 200): continue
   tRes = [ fitFunc.GetParameter(2),fitFunc.GetParError(2)]
   #print h1_deltaT.GetName(), fitFunc.GetParameter(2)
   return tRes


# ====================================
