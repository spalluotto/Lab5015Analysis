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

# ---- style -----
def label_(module):
    if 'LYSO818' in module:
        return 'T1: HPK 25#mum + LYSO818 - unirr'
    elif 'LYSO813' in module:
        return 'T2: HPK 25#mum + LYSO813 - unirr'
    elif 'LYSO816' in module:
        return 'T3: HPK 25#mum + LYSO816 - unirr'
    elif 'LYSO815' in module:
        return 'T2: HPK 25#mum + LYSO815 - irr 2E14'
    elif 'LYSO825' in module:
        return 'T2: HPK 20#mum + LYSO815 - irr 2E14'
    


def color_(module):
    if 'LYSO818' in module:
        return 1
    elif 'LYSO813' in module:
        return 4
    elif 'LYSO816' in module:
        return 2
    elif 'LYSO815' in module:
        return 6
    elif 'LYSO825' in module:
        return 8 



#----- ovs -------

def Iarray(module):
    I = {}
    if 'LYSO815' in module:
        I[2.00] = 0
        I[1.50] = 0
        I[1.25] = 0
        I[1.00] = 0
        I[0.80] = 0
        I[0.60] = 0
    elif 'LYSO825' in module:
        I[2.00] = 0
        I[1.50] = 0
        I[1.25] = 0
        I[1.00] = 0
        I[0.80] = 0
        I[0.60] = 0
    else:
        ovs = [0.5,0.6,0.8,1.0,1.25,1.5,2,3.5]
        for vov in ovs:
            I[vov] = 0 

    return I




def Vovs_eff(ov,label):
    currents = Iarray(label)
    for vov in currents:
        if float(ov) == float(vov):
            return ov - currents[vov]*25





# --- summary plots ----

def good_bars(module, ovs, bars):
    good_bars_ = {}

    if '528' in module:
        good_bars_[3.50] = [2,3,4,5,7,8,9,10,11,12,13] 
        good_bars_[2.00] = [2,3,4,5,7,8,9,10,11,12,13] 
        good_bars_[1.50] = [2,3,4,5,7,8,9,10,11,12,13] 
        good_bars_[1.00] = [2,3,4,5,7,8,9,10,11,12,13] 
        
    elif '813' in module:
        good_bars_[3.50] = [0,1,2,3,4,5,7,8,9,10,11,12,13] 
        good_bars_[2.00] = [0,1,2,3,4,5,7,8,9,10,11,12,13] 
        good_bars_[1.50] = [0,1,2,3,4,5,7,8,9,10,11,12,13] 
        good_bars_[1.00] = [0,2,3,4,5,7,8,9,10,11,12,13] 
        good_bars_[0.80] = [0,2,3,4,5,7,8,9,10,11,12,13]
        good_bars_[0.50] = [0,3,4,5,7,8,10,11,12]
        
    elif '818' in module:
        good_bars_[3.50] = [0,1,2,3,4,5,7,8,9,10,11,12] 
        good_bars_[1.50] = [0,1,2,3,4,5,7,8,9,10,11,12]
        good_bars_[1.00] = [0,2,3,4,5,7,8,9,10,11,12]
        good_bars_[0.80] = [0,2,3,4,5,7,8,9,10,11,12]
        good_bars_[0.50] = [0,3,4,5,7,8,10,11,12]
    
    elif '816' in module:
        good_bars_[3.50] = [0,2,3,4,5,7,8,9,10,11,12] 
        good_bars_[1.50] = [0,2,3,4,5,7,8,9,10,11,12]
        good_bars_[1.00] = [0,2,3,4,5,7,8,9,10,11,12]
        good_bars_[0.80] = [0,3,4,5,7,8,9,10]
        good_bars_[0.50] = [3,4,5,7,8,10,11,12]

    elif '814' in module:
        good_bars_[3.50] = [0,2,3,4,5,7,8,9,10,11,12,13] 
        good_bars_[1.50] = [0,2,3,4,5,7,8,9,10,11,12,13]
        good_bars_[1.00] = [0,2,3,4,5,7,8,9,10,11,12,13]
        good_bars_[0.80] = [0,3,4,5,7,8,9,10,11,12,13]
        good_bars_[0.50] = [0,3,4,5,7,8,9,10,11,12,13]

    elif '815' in module:
        good_bars_[2.00] = [0,3,4,5,7,8,9,10,12,13,15]
        good_bars_[1.50] = [0,3,4,5,7,8,9,11,12,13,15]
        good_bars_[1.25] = [0,3,4,5,7,8,9,11,12,13,15]
        good_bars_[1.00] = [0,3,4,5,7,8,9,11,12,13,15]
        good_bars_[0.80] = [0,3,4,5,7,12,13]
        good_bars_[0.60] = [0,3,4,5,7,12,13]


    elif '825' in module:
        good_bars_[2.00] = [0,1,2,3,4,5,7,8,9,10,11,12]
        good_bars_[1.50] = [0,1,2,3,4,5,7,8,9,10,11,12]
        good_bars_[1.25] = [0,2,3,4,5,7,8,9,10,11,12]
        good_bars_[1.00] = [0,2,3,4,5,7,8,9,10,11,12]
        good_bars_[0.80] = [0,2,3,4,5,7,8,9,10,11,12]
        good_bars_[0.60] = [0,2,3,4,5,7,8,9,10,11,12]
            

    else:
        for vov in ovs:
            good_bars_[vov] = bars 

    return good_bars_

def thickness(module):
    if 'LYSO818' in module:
        return 3.75
    elif 'LYSO813' or 'LYSO815' or 'LYSO825' in module:
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
    return thickness(module)/3


def SR_model(module):
    if 'LYSO818' in module:
        return 7.5
    elif 'LYSO813' in module:
        return 7
    elif 'LYSO816' in module:
        return 6.5




#---- utils ----
def intersection(lst1,lst2):
    lstIntersection = [value for value in lst1 if value in lst2] 
    return lstIntersection
def union(lst1,lst2):
    return lst1 + list(set(lst2) - set(lst1))



