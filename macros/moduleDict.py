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
        return 'T1: HPK 25#mum + LYSO818'
    elif 'LYSO813' in module:
        return 'T2: HPK 25#mum + LYSO813'
    elif 'LYSO816' in module:
        return 'T3: HPK 25#mum + LYSO816'

    # if 'LYSO818' in module:
    #     return 'HPK 25#mum T1'
    # elif 'LYSO813' in module:
    #     return 'HPK 25#mum T2'
    # elif 'LYSO816' in module:
    #     return 'HPK 25#mum T3'


def color_(module):
    if 'LYSO818' in module:
        return 1
    elif 'LYSO813' in module:
        return 4
    elif 'LYSO816' in module:
        return 2


#----- ovs -------

def Iarray(module):
    if 'LYSO818' in module:
        return 0
    elif 'LYSO813' in module:
        return 0
    elif 'LYSO816' in module:
        return 0
    else:
        print 'ERROR: could not find the array current'
        return None


def Vovs_eff(ov,label):
    I = Iarray(label)
    VovEff = ov - I*25
    return VovEff





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
        good_bars_[0.50] = [0,3,4,5,7,8]
        
    elif '818' in module:
        good_bars_[3.50] = [0,1,2,3,4,5,7,8,9,10,11,12] 
        good_bars_[1.50] = [0,1,2,3,4,5,7,8,9,10,11,12]
        good_bars_[1.00] = [0,2,3,4,5,7,8,9,10,11,12]
        good_bars_[0.80] = [0,2,3,4,5,7,8,9,10,11,12]
        good_bars_[0.50] = [0,3,4,5,7]
    
    elif '816' in module:
        good_bars_[3.50] = [0,2,3,4,5,7,8,9,10,11,12] 
        good_bars_[1.50] = [0,2,3,4,5,7,8,9,10,11,12]
        good_bars_[1.00] = [0,2,3,4,5,7,8,9,10,11,12]
        good_bars_[0.80] = [0,3,4,5,7,8,9,10]
        good_bars_[0.50] = [3,4,5,7]

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




#---- utils ----
def intersection(lst1,lst2):
    lstIntersection = [value for value in lst1 if value in lst2] 
    return lstIntersection
def union(lst1,lst2):
    return lst1 + list(set(lst2) - set(lst1))



