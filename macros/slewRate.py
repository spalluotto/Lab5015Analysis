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
        tmax = min(g1.GetX()[imin+npoints],3.)
        nmax = imin+npoints+1
    else:
        tmax = 3
        nmax = g1.GetN()

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
