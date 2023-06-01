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
    


def thickness(module):
    lyso_ref = lyso_(module)
    if 'LYSO818' == lyso_ref or 'LYSO819' == lyso_ref or 'LYSO829' == lyso_ref:
        return 3.75
    elif 'LYSO813' == lyso_ref or 'LYSO815'==lyso_ref  or 'LYSO825' == lyso_ref or 'LYSO820' == lyso_ref:
        return 3
    elif 'LYSO816' == lyso_ref or 'LYSO817' == lyso_ref:
        return 2.4
    else:
        print 'ERROR CANNOT FIND THICKNESS'
        return 'ERROR'
        


def light_output(module):
    if 'LYSO818' in module:
        return 2410
    elif 'LYSO813' in module:
        return 2250
    elif 'LYSO816' in module:
        return 2190
    elif 'LYSO815' in module:
        return 2250
    elif 'LYSO825' in module:
        return 2050
    elif 'LYSO819' in module:
        return 2410
    elif 'LYSO817' in module:
        return 2190
    elif 'LYSO820' in module:
        return 2400
    elif 'LYSO829' in module:
        return 2410



# ------ stoch ref -----
def stoch_reference(module):
    if 'LYSO818' in module:
        return 0
    elif 'LYSO813' in module:
        return 0
    elif 'LYSO816' in module:
        return 0
    elif 'LYSO815' in module:
        return 30
    elif 'LYSO825' in module:
        return 35
    elif 'LYSO819' in module:
        return 30
    elif 'LYSO817' in module:
        return 0
    elif 'LYSO820' in module:
        return 30
    elif 'LYSO829' in module:
        return 35



def ov_reference(module):
    if 'LYSO818' in module:
        return 3.5
    elif 'LYSO813' in module:
        return 3.5
    elif 'LYSO816' in module:
        return 3.5
    elif 'LYSO815' in module:
        return 1
    elif 'LYSO825' in module:
        return 1
    elif 'LYSO819' in module:
        return 1
    elif 'LYSO817' in module:
        return 1
    elif 'LYSO820' in module:
        return 1
    elif 'LYSO829' in module:
        return 1




# ------- style --------
    
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
    elif 'LYSO817' in module:
        return 40
    elif 'LYSO820' in module:
        return 42
    elif 'LYSO829' in module:
        return 44





# ---- not used ----



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


def SR_model(module):
    if 'LYSO818' in module:
        return 7.5
    elif 'LYSO813' in module:
        return 7
    elif 'LYSO816' in module:
        return 6.5







# --------------------------------------------------------
# --------------------------------------------------------
# --------------------------------------------------------
# --------------------------------------------------------
# --------------------------------------------------------




def irradiation(module):
    if 'nonIrr' in sipm_(module):
        return 'non-irr'
    elif 'E1' in sipm_(module):
        tmp = sipm_(module).split('_')[1]
        return 'irr '+tmp
    else:
        print 'not sure. Which irradiation?'
        return 0

        return 'ERROR'
    


def temperature_(module):
    if '_T' in module:
        tmp = module.split("_T")[1].split("C")[0]
        return tmp
    else:
        print 'ERROR: CANNOT FIND TEMPERATURE IN THE NAME'
        return 'ERROR'







#----- ovs -------

def getVovEffDCR(module, ov) :

    ov_temp = round(5*round(float(ov)/5,2),2)
    ov_set = '%.2f'%float(ov_temp)

    irrad = irradiation(module)
    temp = temperature_(module)
    
    if 'non-irr' in irrad:
        return([ov_set,0])

    elif 'irr' in irrad:
        # Import file with VovEff and DCR
        with open('/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_H8_May2023/VovsEff.json', 'r') as f:
            data = json.load(f) 

        if not data[sipm_(module)+'_'+lyso_(module)+'_T'+temp+'C_A'][ov_set][0]:
            print 'ERROR:   ',module,'  not in json file!!!'
            return ([ov_set,0,0])
        else:
            ov_eff_A = float(data[sipm_(module)+'_'+lyso_(module)+'_T'+temp+'C_A'][ov_set][0])
            dcr_A    = float(data[sipm_(module)+'_'+lyso_(module)+'_T'+temp+'C_A'][ov_set][1])
            ov_eff_B = float(data[sipm_(module)+'_'+lyso_(module)+'_T'+temp+'C_B'][ov_set][0])
            dcr_B    = float(data[sipm_(module)+'_'+lyso_(module)+'_T'+temp+'C_B'][ov_set][1])

            current_A= float(data[sipm_(module)+'_'+lyso_(module)+'_T'+temp+'C_A'][ov_set][2])
            current_B= float(data[sipm_(module)+'_'+lyso_(module)+'_T'+temp+'C_B'][ov_set][2])
            current = 0.5*(current_A+current_B)

            ov_eff =  0.5*(ov_eff_A+ov_eff_B)
            dcr    =  0.5*(dcr_A+dcr_B)
            return ([ov_eff, dcr, current])      

    else:
        print 'ERROR: CANNOT FIND WHICH IRRADIATION'
        return 'ERROR'


def Vovs_eff(module, ov):
    ov_set_ = '%.2f'%float(ov)
    if 'non-irr' in irradiation(module):
        VovEff_ = float(ov_set_)
    else:    
        VovEff_ = getVovEffDCR(module, ov_set_)[0]
    return VovEff_


def DCR(module, ov):
    ov_set_ = '%.2f'%float(ov)
    if 'non-irr' in irradiation(module):
        DCR_ = 0
    else:    
        DCR_ = getVovEffDCR(module,ov_set_)[1]

    return DCR_


def current_(module, ov):
    ov_set_ = '%.2f'%float(ov)
    if 'non-irr' in irradiation(module):
        cur_ = 0
    else:    
        cur_ = getVovEffDCR(module,ov_set_)[2]

    return cur_



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


def Npe_frac(module):
    return thickness(module)/3



# ---- style -----
def label_(module):
    tmp = 'T'+str(type_(module))+': '+sipm_cell_size(module)+' '+irradiation(module)+'+ '+lyso_(module)+' + T'+temperature_(module)+'C'
    #tmp = 'T'+str(type_(module))+'  :  '+sipm_cell_size(module)+'   +   '+lyso_(module)
    return tmp






#---- utils ----
def intersection(lst1,lst2):
    lstIntersection = [value for value in lst1 if value in lst2] 
    return lstIntersection
def union(lst1,lst2):
    return lst1 + list(set(lst2) - set(lst1))



# -----------------------
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
        good_bars_[2.50] = [0,3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[2.00] = [0,3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[1.50] = [0,3,4,5,7,8,9,11,12,13,15]
        good_bars_[1.25] = [0,3,4,5,7,8,9,11,12,13,15]
        good_bars_[1.00] = [0,3,4,5,7,8,11,12,13,15]
        good_bars_[0.80] = [0,3,4,5,7,12,13]
        good_bars_[0.60] = [0,4,5,7,12]
            
    elif '819' in module:
        good_bars_[2.50] = [3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[2.00] = [0,2,3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[1.50] = [0,2,3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[1.25] = [0,3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[1.00] = [0,3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[0.80] = [0,3,4,5,7,8,9,12,13,15]
        good_bars_[0.60] = [0,3,4,5,7,8,9,12,13,15]


    elif '829' in module:
        good_bars_[3.00] = [1,2,3,4,5,6,7,10,11,13,14,15]
        good_bars_[2.50] = [0,1,2,3,4,5,7,8,9,10,11,12]
        good_bars_[2.00] = [1,2,3,4,5,7,8,9,10,11,12]
        good_bars_[1.50] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        good_bars_[1.25] = [0,2,3,4,5,7,8,9,10,11,12]
        good_bars_[1.00] = [0,2,3,4,5,7,8,9,10,11,12,]
        good_bars_[0.80] = [0,3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[0.60] = [0,2,3,4,5,7,8,9,10,11,12]
            
    elif '817' in module:
        good_bars_[2.50] = [3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[2.00] = [0,2,3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[1.50] = [0,2,3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[1.25] = [0,3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[1.00] = [0,3,4,5,7,8,9,11,12,13,15]
        good_bars_[0.80] = [0,3,4,5,7,8,9,12,13,15]
        good_bars_[0.60] = [0,3,4,5,7,8,9,12,13]


    elif '820' in module:
        good_bars_[3.50] = [0,1,2,3,4,5,7,8,9,10,11,12,13,14,15]
        good_bars_[1.50] = [0,1,2,3,4,5,7,8,9,10,11,12,13,14,15]
        good_bars_[0.80] = [0,3,4,5,7,8,9,10,11,12,13,15]
        good_bars_[0.60] = [0,3,4,5,7,8,9,10,11,12,13,15]


    else:
        for vov in ovs:
            good_bars_[vov] = bars 

    return good_bars_
