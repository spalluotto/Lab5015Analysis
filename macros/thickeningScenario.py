#! /usr/bin/env python
import os
import shutil
import glob
import math
import array
import sys
import time
import argparse

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
        scenario.color = 1


plotsdir = '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots'

### ----------------------     EoL    ----------------------------- #####
#--- T1 T2 T3
standard_EoL = scenario()
standard_EoL.sipmTypes = ['HPK_1E14_LYSO819','HPK_2E14_LYSO815','HPK_1E14_LYSO817']
standard_EoL.fname = '%s/compareTimeResolution_vs_Vov_EoL_T1_T2_T3.root'%plotsdir
standard_EoL.extraName  = ['_angle32_T-22C', '_angle52_T-35C', '_angle64_T-22C']
standard_EoL.angles = [32, 52, 64]
standard_EoL.label = 'T1 T2 T3'
standard_EoL.posCor = [7,10,15]
standard_EoL.color = 1

#--- T1 T2 T2
mixed_EoL = scenario()
mixed_EoL.sipmTypes = ['HPK_1E14_LYSO819','HPK_2E14_LYSO815','HPK_2E14_LYSO815']
mixed_EoL.fname = '%s/compareTimeResolution_vs_Vov_EoL_T1_T2_T2.root'%plotsdir
mixed_EoL.extraName  = ['_angle32_T-22C', '_angle52_T-35C', '_angle64_T-35C']
mixed_EoL.angles = [32, 52, 64]
mixed_EoL.label = 'T1 T2 T2'
mixed_EoL.posCor = [7,10,15]
mixed_EoL.color = 2

#--- T1 T1 T1
allT1_EoL = scenario()
allT1_EoL.sipmTypes = ['HPK_1E14_LYSO819','HPK_1E14_LYSO819','HPK_1E14_LYSO819']
allT1_EoL.fname = '%s/compareTimeResolution_vs_Vov_EoL_T1_T1_T1.root'%plotsdir
allT1_EoL.extraName  = ['_angle32_T-22C', '_angle52_T-22C', '_angle64_T-22C']
allT1_EoL.angles = [32, 52, 64]
allT1_EoL.label = 'T1 T1 T1'
allT1_EoL.posCor = [7,10,15]
allT1_EoL.color = 417








### ----------------------     BTLlike    ----------------------------- #####
#--- T1 T2 T3
standard_BTLlike = scenario()
standard_BTLlike.sipmTypes = ['HPK_1E14_LYSO819','HPK_2E14_LYSO815','HPK_1E14_LYSO817']
standard_BTLlike.fname = '%s/compareTimeResolution_vs_Vov_BTLlike_T1_T2_T3.root'%plotsdir
standard_BTLlike.extraName  = ['_angle32_T-32C', '_angle52_T-40C', '_angle64_T-32C']
standard_BTLlike.angles = [32, 52, 64]
standard_BTLlike.label = 'T1 T2 T3'
standard_BTLlike.posCor = [7,10,15]
standard_BTLlike.color = 1

#--- T1 T1 T1
allT1_BTLlike = scenario()
allT1_BTLlike.sipmTypes = ['HPK_1E14_LYSO819','HPK_1E14_LYSO819','HPK_1E14_LYSO819']
allT1_BTLlike.fname = '%s/compareTimeResolution_vs_Vov_BTLlike_T1_T1_T1.root'%plotsdir
allT1_BTLlike.extraName  = ['_angle32_T-32C', '_angle52_T-32C', '_angle64_T-32C']
allT1_BTLlike.angles = [32, 52, 64]
allT1_BTLlike.label = 'T1 T1 T1'
allT1_BTLlike.posCor = [7,10,15]
allT1_BTLlike.color = 417




