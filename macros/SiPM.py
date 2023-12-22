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

    elif '528' in lyso_:
        return 'HPK-MS'









def PDE_(ov, sipm, flag='1'):
    irr = irradiation(sipm)

    if (irr == '2E14' and 'HPK' in sipm): k = 0.78 # 22% PDE reduction for HPK SiPMs irradiated 2E14  
    elif (irr == '1E14' and 'HPK' in sipm): k = 0.89 # 11% PDE reduction for HPK SiPMs irradiated 1E14 ?(assume that for 1E14 is half of 2E14) 
    else:
        k = 1

    if flag == '0':
        k = 1
        

    type = sipm_type(sipm)
    if type == 'HPK-MS':
        return k * 0.389 * ( 1. - math.exp(-1.*0.593*ov) )
    elif type == 'FBK-MS':
        return k * 0.419907 * ( 1. - math.exp(-1.*0.3046*ov) )
    # -- new cell size --
    elif type == 'HPK-ES2-20um':
        return k * 0.576 * ( 1. - math.exp(-1.*0.625*ov) )
    elif type == 'HPK-ES2-25um':
        return k * 0.638 * ( 1. - math.exp(-1.*0.651*ov) )
    elif type == 'HPK-ES2-30um':
        return k * 0.653 * ( 1. - math.exp(-1.*0.728*ov) )
    # -- low Cg --
    elif type == 'HPK-ES3-20um':
        return k * 0.568 * ( 1. - math.exp(-1.*0.588*ov) )
    elif type == 'HPK-ES3-25um':
        return k * 0.638 * ( 1. - math.exp(-1.*0.589*ov) )
    else:
        print('CANNOT FIND PDE')









def Gain_(Vov,sipm,flag='1'):
    irr = irradiation(sipm)

    if (irr == '2E14' and 'HPK' in sipm): k = 0.92    # gain reduction for HPK 2E14 irradiated SiPMs 
    elif (irr == '1E14' and 'HPK' in sipm): k = 0.96  # gain reduction for HPK 1E14 irradiated SiPMs (assume that for 1E14 is half of 2E14)
    else:
        k = 1

    if flag == '0':
        k = 1

    type = sipm_type(sipm)
    if type == 'HPK-MS':
        return k * 36890.187 + 97602.9*Vov
    elif type == 'FBK-MS':
        return k * 94954.6*(ov+0.512167)
    # -- new cell size --
    elif type == 'HPK-ES2-20um':
        return k * 6.234E04 + 1.787E05*Vov
    elif type == 'HPK-ES2-25um':
        return k * 7.044E04 + 2.895E05*Vov
    elif type == 'HPK-ES2-30um':
        return k * 9.067E04 + 4.020E05*Vov

    # -- low Cg --
    elif type == 'HPK-ES3-20um':
        return k * 5.731E04 + 1.759E05*Vov
    elif type == 'HPK-ES3-25um':
        return k * 7.857E04 + 2.836E05*Vov
    else:
        print('CANNOT FIND GAIN')




