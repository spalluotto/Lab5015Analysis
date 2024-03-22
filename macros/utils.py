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

import math
import ROOT

import CMS_lumi, tdrstyle

from slewRate import *
from SiPM import *
from moduleDict import *

def draw_logo():
    logo_x = 0.16
    logo = ROOT.TLatex()
    logo.SetNDC()
    logo.SetTextSize(0.045) 
    logo.SetTextFont(62)
    logo.DrawText(logo_x,0.95,'CMS') 
    logo.SetTextFont(52)
    logo.DrawText(logo_x+0.07, 0.95, '  MTD Test Beam')
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


def remove_points_beyond_rms(g, rms_thr):
    if not g:
        return
    n      = g.GetN()
    x_vals = g.GetX()
    y_vals = g.GetY()
    x_errs = g.GetEX()
    y_errs = g.GetEY()
    mean   = g.GetMean(2)
    rms    = g.GetRMS(2)
    new_g  = ROOT.TGraphErrors()
    for i in range(g.GetN()):
        if abs(y_vals[i] - mean) <= rms_thr * rms:
            new_g.SetPoint(new_g.GetN(), x_vals[i], y_vals[i])
            new_g.SetPointError(new_g.GetN()-1, x_errs[i], y_errs[i])
        else:
            print(" ~~~~~~~~~~~   point at ", x_vals[i], ' removed')

    return new_g


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
ROOT.gStyle.SetOptFit(111)
