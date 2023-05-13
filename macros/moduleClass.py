#! /usr/bin/env python
import os
import shutil
import glob
import math
import array
import sys
import time
import argparse
from ROOT import *



#---- utils ----
def intersection(lst1,lst2):
    lstIntersection = [value for value in lst1 if value in lst2] 
    return lstIntersection
def union(lst1,lst2):
    return lst1 + list(set(lst2) - set(lst1))





class module:
    def __init__(self):
        module.label = ''
        module.thickness = 100
        module.light_output = 2100
        module.tau_decay = 41
        module.tau_rise = 15
        

        module.good_bars_ = {}
        module.color = 1
        module.Npe_frac = 1
        module.ovs = []
        module.angles = []
        module.Iarray = {}

        module.summaryPlot = ''
        module.drawPulseShape = ''
        module.plot_tres = ''






# ---- LYSO 528 --------
conf3 = module()
conf3.label = 'T2: HPK 15#mum + LYSO528'
conf3.thickness = 3
conf3.light_output = 1265
conf3.good_bars_ = {
        3.50 : [2,3,4,5,7,8,9,10,11,12,13] 
        2.00 : [2,3,4,5,7,8,9,10,11,12,13] 
        1.50 : [2,3,4,5,7,8,9,10,11,12,13] 
        1.00 : [2,3,4,5,7,8,9,10,11,12,13] 
}
conf3.color = 4
conf3.ovs = [1,1.5,2,3.5]
conf3.angles = [52]





# ---- LYSO 813 -------- 
conf4 = module()
conf4.label = 'T2: HPK 25#mum + LYSO813'
conf4.thickness = 3
conf4.light_output = 2418
conf4.good_bars_ = {
    3.50 : [0,1,2,3,4,5,7,8,9,10,11,12,13] 
    2.00 : [0,1,2,3,4,5,7,8,9,10,11,12,13] 
    1.50 : [0,1,2,3,4,5,7,8,9,10,11,12,13] 
    1.00 : [0,2,3,4,5,7,8,9,10,11,12,13] 
    0.80 : [0,2,3,4,5,7,8,9,10,11,12,13]
    0.50 : [0,3,4,5,7,8]
}
conf4.color = 4
conf4.ovs = [0.5, 0.8, 1, 1.5, 2, 3.5]
conf4.angles = [52,64]




# ---- LYSO 818 -------- 
conf5 = module()
conf5.label = 'T1: HPK 25#mum + LYSO818'
conf5.thickness = 3.75
conf5.light_output = 3020
conf5.good_bars_ = {
        3.50 : [0,1,2,3,4,5,7,8,9,10,11,12] 
        1.50 : [0,1,2,3,4,5,7,8,9,10,11,12]
        1.00 : [0,2,3,4,5,7,8,9,10,11,12]
        0.80 : [0,2,3,4,5,7,8,9,10,11,12]
        0.50 : [0,3,4,5,7]
}
conf5.color = 1
conf5.ovs = [0.5, 0.8, 1.5, 3.5]
conf5.angles = [32,52,64]
conf5.Npe_frac = conf5.thickness/3






# ---- LYSO 816 -------- 
conf6 = module()
conf6.label = 'T3: HPK 25#mum + LYSO816'
conf6.thickness = 2.4
conf6.light_output = 1800
conf6.good_bars_ = {
        3.50 : [0,2,3,4,5,7,8,9,10,11,12] 
        1.50 : [0,2,3,4,5,7,8,9,10,11,12]
        1.00 : [0,2,3,4,5,7,8,9,10,11,12]
        0.80 : [0,3,4,5,7,8,9,10]
        0.50 : [3,4,5,7]
}
conf6.color = 2
conf6.ovs = [0.5, 0.8, 1.5, 3.5]
conf6.angles = [52]
conf6.Npe_frac = conf6.thickness/3







def Vovs_eff(ov,module):
    I = module.Iarray(module)[ov]
    VovEff = ov - I*25
    return VovEff




    elif '814' in module:
        good_bars_[3.50] = [0,2,3,4,5,7,8,9,10,11,12,13] 
        good_bars_[1.50] = [0,2,3,4,5,7,8,9,10,11,12,13]
        good_bars_[1.00] = [0,2,3,4,5,7,8,9,10,11,12,13]
        good_bars_[0.80] = [0,3,4,5,7,8,9,10,11,12,13]
        good_bars_[0.50] = [0,3,4,5,7,8,9,10,11,12,13]
            

    else:
        for vov in ovs:
            good_bars_[vov] = bars 

    return good_bars_

def thickness(module):
    if 'LYSO818' in module:
        return 3.75
    elif 'LYSO813' in module:
        return 3
    elif 'LYSO816' in module:
        return 2.4

def light_output(module):
    if 'LYSO818' in module:
        return 2249
    elif 'LYSO813' in module:
        return 2418
    elif 'LYSO816' in module:
        return 2337
    
def tau_decay(module):
    if 'LYSO818' in module:
        return 41 
    elif 'LYSO813' in module:
        return 41
    elif 'LYSO816' in module:
        return 41

def tau_rise(module):
    if 'LYSO818' in module:
        return 14 
    elif 'LYSO813' in module:
        return 14
    elif 'LYSO816' in module:
        return 14

def Npe_frac(module):
    if 'LYSO818' in module:
        return 3.75/3
    elif 'LYSO813' in module:
        return 3/3
    elif 'LYSO816' in module:
        return 2.4/3

def SR_model(module):
    if 'LYSO818' in module:
        return 7.5
    elif 'LYSO813' in module:
        return 7
    elif 'LYSO816' in module:
        return 6.5


