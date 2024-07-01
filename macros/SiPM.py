#! /usr/bin/env python
import math
from moduleDict import *



def sipm_type(lyso_):
    if '828' in lyso_ or '824' in lyso_ or '826' in lyso_:
        return 'HPK-ES3-25um'

    elif '818' in lyso_ or '813' in lyso_ or '816' in lyso_ or '828' in lyso_ or '826' in lyso_ or '815' in lyso_ or '819' in lyso_ or '817' in lyso_ or '829' in lyso_ or '100056' in lyso_ or '300032' in lyso_:
        return 'HPK-ES2-25um'

    elif '814' in lyso_ or '825' in lyso_:
        return 'HPK-ES2-20um'

    elif '824' in lyso_:
        return 'HPK-ES3-25um'

    elif '820' in lyso_ or '200104' in lyso_:
        return 'HPK-ES2-30um'

    elif '528' in lyso_ or '796' in lyso_:
        return 'HPK-MS'







# ----------------------
# ----- PDE ------------
# ----------------------

def PDE_(ov, sipm, flag='1'):
    type = sipm_type(sipm)
    irr = irradiation(sipm)


    ###
    # Market Survey
    if (irr == '2E14' and 'HPK-MS' in type): k = 0.78 # 22% PDE reduction for HPK SiPMs irradiated 2E14   
    elif (irr == '1E14' and 'HPK-MS' in type): k = 0.89 # 11% PDE reduction for HPK SiPMs irradiated 1E14 ?(assume that for 1E14 is half of 2E14) 

    # PDE improved
    elif (irr == '2E14' and 'HPK-ES' in type): k = 0.85 # 15% PDE reduction for HPK SiPMs irradiated 2E14  - large cell-size 
    elif (irr == '1E14' and 'HPK-ES' in type): k = 0.925 # %7.5% PDE reduction for HPK SiPMs irradiated 1E14 ?(assume that for 1E14 is half of 2E14) 
    else:
        k = 1

    # when non irr are specified with the flag
    if flag == '0':
        k = 1

    pde_val = 0
    
    # Market Survey

    if    type == "HPK-MS": 
        pde_val =  k * 0.389 * ( 1. - math.exp(-1.*0.593*ov) )

    # --- FBK
    elif  type == "FBK-MS": 
        pde_val =  k * 0.419907 * ( 1. - math.exp(-1.*0.3046*ov) )
    elif  type == "FBK-W4S": 
        pde_val =  k * 0.411 * ( 1. - math.exp(-1.*0.191*ov) )/1.071
    elif  type == "FBK-W4C": 
        pde_val =  k * 0.490 * ( 1. - math.exp(-1.*0.225*ov) )/1.071

        
    # PDE improved   
    elif  type == "HPK-ES2-20um":
        pde_val =  k * 0.576 * ( 1. - math.exp(-1.*0.625*ov) )
    elif  type == "HPK-ES2-25um":
        pde_val =  k * 0.638 * ( 1. - math.exp(-1.*0.651*ov) )
    elif  type == 'HPK-ES2-30um':
        pde_val =  k * 0.653 * ( 1. - math.exp(-1.*0.728*ov) )
        
    # -- low Cg -- 
    elif  type == "HPK-ES3-20um":
        pde_val =  k * 0.568 * ( 1. - math.exp(-1.*0.588*ov) )
    elif  type == "HPK-ES3-25um":
        pde_val =  k * 0.638 * ( 1. - math.exp(-1.*0.589*ov) )
    elif  type == "HPK-ES3-30um":
        pde_val =  k * 0.653 * ( 1. - math.exp(-1.*0.728*ov) )
    else:
        print("\n ERROR : SiPM type not found for PDE evaluation")        

    return pde_val







# ----------------------
# ----- Gain -----------
# ----------------------

def Gain_(ov,sipm,flag='1'):
    irr = irradiation(sipm)
    type = sipm_type(sipm)

    ####
    # Market Survey
    if (irr == '2E14' and 'HPK-MS' in type): k = 0.92       # 8% for 2E14
    elif (irr == '1E14' and 'HPK-MS' in type): k = 0.96     # 4% for 1E14

    # PDE improved
    elif (irr == '2E14' and 'HPK-ES' in type): k = 0.95    # 5% for 2E14
    elif (irr == '1E14' and 'HPK-ES' in type): k = 0.975   # assume that for 1E14 is half of 2E14
    else:
        k=1

    if flag == '0':
        k = 1


    gain_val = 0

    # Market Survey    
    if   (type == "HPK-MS"): 
        gain_val =  k * 36890.187 + 97602.9*ov

    # --- FBK 
    elif (type == "FBK-MS"): 
        gain_val =  k * (94954.6*(ov+0.512167))
    elif (type == "FBK-W4S"): 
        gain_val =  k * (91541.7*(ov+0.408182))
    elif (type == "FBK-W4C"): 
        gain_val =  k * (91541.7*(ov+0.408182))

    # PDE improved  
    elif   (type == "HPK-ES2-20um"): 
        gain_val =  k * (6.234E04 + 1.787E05*ov)
    elif   (type == "HPK-ES2-25um"): 
        gain_val =  k * (7.044E04 + 2.895E05*ov)
    elif type == 'HPK-ES2-30um':
        gain_val =  k * 9.067E04 + 4.020E05*ov
        
    # -- low Cg --  
    elif   (type == "HPK-ES3-20um"): 
        gain_val =  k * (5.731E04 + 1.759E05*ov)
    elif   (type == "HPK-ES3-25um"): 
        gain_val =  k * (7.857E04 + 2.836E05*ov)
    elif   (type == "HPK-ES3-30um"): 
        gain_val =  k * (9.067E04 + 4.020E05*ov)

    else:
        print("\n ERROR : SiPM type not found for Gain evaluation")        

    return gain_val




