#! /usr/bin/env python
import math
def PDE(ov, sipm, irr='0'):
    k = 1.
    if (irr == '2E14' and 'HPK' in sipm): k = 0.78 # 22% PDE reduction for HPK SiPMs irradiated 2E14   
    if ('HPK' in sipm):
        return k * 1.0228 * 0.384 * ( 1. - math.exp(-1.*0.583*ov) ) # 1.0228 factor to account for LYSO emission spectrum
    # FBK-MS
    #if ('FBK' in sipm):
    #    return k * 0.8847*0.466 * ( 1. - math.exp(-1.*0.314*ov) ) # 0.8847 factor to account for LYSO emission spectrum
    #FBK W4C
    if ('FBK' in sipm):
        return k * 0.490 * ( 1. - math.exp(-1.*0.225*ov) )/1.071 # 1.071 factor to account for bech calib, convolution PDE with LYSO already accounted for
    elif('C25' in sipm):
        return 0.638 * ( 1. - math.exp(-1.*0.651*ov) )


def Gain(ov, sipm, irr='0'):
    k = 1.
    if (irr == '2E14' and 'HPK' in sipm): k = 0.92 # gain reduction for HPK 2E14 irradiated SiPMs 
    if ('HPK' in sipm):
        return k*(36890. + 97602.*ov) # HPK
    # FBK-MS
    #if ('FBK' in sipm):
    #    return k*(50739. + 95149.*ov) # FBK-MS
    # FBK-W4C 
    if ('FBK' in sipm):
        return 91541.7*(ov+0.408182) # FBK-W4C

    elif   ('C25' in sipm): 
        return 7.044E04 + 2.895E05*ov
