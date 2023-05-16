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
from ROOT import *


def lyso_(module):
    if 'LYSO818' in module:
        return 'LYSO818'
    elif 'LYSO813' in module:
        return 'LYSO813'
    elif 'LYSO816' in module:
        return 'LYSO816'
    elif 'LYSO815' in module:
        return 'LYSO815'
    elif 'LYSO825' in module:
        return 'LYSO825'
    elif 'LYSO819' in module:
        return 'LYSO819'
    elif 'LYSO817' in module:
        return 'LYSO817'
    elif 'LYSO820' in module:
        return 'LYSO820'
    elif 'LYSO829' in module:
        return 'LYSO829'

def sipm_(module):
    if 'LYSO818' in module:
        return 'HPK_nonIrr'
    elif 'LYSO813' in module:
        return 'HPK_nonIrr'
    elif 'LYSO816' in module:
        return 'HPK_nonIrr'
    elif 'LYSO815' in module:
        return 'HPK_2E14'
    elif 'LYSO825' in module:
        return 'HPK_2E14'
    elif 'LYSO819' in module:
        return 'HPK_1E14'
    elif 'LYSO817' in module:
        return 'HPK_1E14'
    elif 'LYSO820' in module:
        return 'HPK_nonIrr'
    elif 'LYSO829' in module:
        return 'HPK_1E13'



def sipm_cell_size(module):
    if 'LYSO818' in module:
        return 'HPK 25#mum'
    elif 'LYSO813' in module:
        return 'HPK 25#mum'
    elif 'LYSO816' in module:
        return 'HPK 25#mum'
    elif 'LYSO815' in module:
        return 'HPK 25#mum'
    elif 'LYSO825' in module:
        return 'HPK 20#mum'
    elif 'LYSO819' in module:
        return 'HPK 25#mum'
    elif 'LYSO817' in module:
        return 'HPK 25#mum'
    elif 'LYSO820' in module:
        return 'HPK 30#mum'
    elif 'LYSO829' in module:
        return 'HPK 25#mum'
    



def irradiation(module):
    if 'nonIrr' in sipm_(module):
        return 'non-irr'
    elif 'E1' in sipm_(module):
        tmp = sipm_(module).split('_')[1]
        return 'irr '+tmp
    else:
        print 'not sure. Which irradiation?'
        return 0

        return 'non-irr'
    


def temperature_(module):
    if '_T' in module:
        tmp = module.split("_T")[1].split("C")[0]
        return tmp
    else:
        print 'ERROR: CANNOT FIND TEMPERATURE IN THE NAME'
        return 'ERROR'

#----- ovs -------

def getVovEffDCR(module, ov_set) :
    irrad = irradiation(module)
    temp = temperature_(module)

    if 'non-irr' in irrad:
        return([ov_set,0])

    elif 'irr' in irrad:
        # Import file with VovEff and DCR
        with open('/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_H8_May2023/VovsEff.json', 'r') as f:
            data = json.load(f) 

        ov_eff_A = float(data[lyso_(module)+'_'+sipm_(module)+'_T'+temp+'C_A'][ov_set][0])
        dcr_A    = float(data[lyso_(module)+'_'+sipm_(module)+'_T'+temp+'C_A'][ov_set][1])
        ov_eff_B = float(data[lyso_(module)+'_'+sipm_(module)+'_T'+temp+'C_B'][ov_set][0])
        dcr_B    = float(data[lyso_(module)+'_'+sipm_(module)+'_T'+temp+'C_B'][ov_set][1])
        ov_eff =  0.5*(ov_eff_A+ov_eff_B)
        dcr    =  0.5*(dcr_A+dcr_B)
        return ([ov_eff, dcr])      

    else:
        print 'ERROR: CANNOT FIND WHICH IRRADIATION'
        return 'ERROR'


def Vovs_eff(module, ov):
    if 'non-irr' in irradiation(module):
        VovEff = ov
    else:    
        VovEff = getVovEffDCR(module,('%.02f'%ov))[0]
    return VovEff


def DCR(module, temp, ov):
    if 'non-irr' in irradiation(module):
        DCR_ = 0
    else:    
        DCR_ = getVovEffDCR(module,temp,('%.02f'%ov))[1]

    return DCR_



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
    if 'LYSO818' in module or 'LYSO819' in module:
        return 3.75
    elif 'LYSO813' or 'LYSO815' or 'LYSO825' in module:
        return 3
    elif 'LYSO816' in module or 'LYSO817' in module:
        return 2.4



def type_(module):
    if thickness(module) == 3.75:
        return 1
    elif thickness(module) == 3:
        return 2
    elif thickness(module) == 2.4:
        return 3
    else:
        print 'ERROR: TYPE NOT DEFINED'
        return 'ERROR'





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

# ---- style -----
def label_(module):
    tmp = 'T'+str(type_(module))+': '+sipm_cell_size(module)+' '+irradiation(module)+'+ '+lyso_(module)+' + T'+temperature_(module)+'C'
    return tmp


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
    elif 'LYSO819' in module:
        return 9

    






#---- utils ----
def intersection(lst1,lst2):
    lstIntersection = [value for value in lst1 if value in lst2] 
    return lstIntersection
def union(lst1,lst2):
    return lst1 + list(set(lst2) - set(lst1))



