#! /usr/bin/env python
import math




def sipm_type(lyso_):
    if '828' in lyso_ or '824' in lyso_ or '826' in lyso_:
        return 'HPK-ES3-25um'

    elif '818' in lyso_ or '813' in lyso_ or '816' in lyso_ or '828' in lyso_ or '826' in lyso_ or '815' in lyso_ or '819' in lyso_ or '817' in lyso_:
        return 'HPK-ES2-25um'

    elif '814' in lyso_ or '825' in lyso_:
        return 'HPK-ES2-20um'

    elif '824' in lyso_:
        return 'HPK-ES3-25um'

    elif '820' in lyso_:
        return 'HPK-ES2-30um'

    elif '528' in lyso_:
        return 'HPK-MS'


def Gain(Vov,_lyso):
    type = sipm_type(_lyso)
    if type == 'HPK-ES1-15um':
        return 36890. + 97602.*Vov
    elif type == 'FBK-MS':
        return 94954.6*(ov+0.512167)
    # -- new cell size --
    elif type == 'HPK-ES2-20um':
        return 6.234E04 + 1.787E05*Vov
    elif type == 'HPK-ES2-25um':
        return 7.044E04 + 2.895E05*Vov
    elif type == 'HPK-ES2-30um':
        return 9.067E04 + 4.020E05*ov
    # -- low Cg --
    elif type == 'HPK-ES3-20um':
        return 5.731E04 + 1.759E05*Vov
    elif type == 'HPK-ES3-25um':
        return 7.857E04 + 2.836E05*Vov
    else:
        print 'CANNOT FIND GAIN'




def PDE(ov, sipm, irr='0'):
    type = sipm_type(sipm)
    if type == 'HPK-ES1-15um':
        return 0.389 * ( 1. - math.exp(-1.*0.593*ov) )
    elif type == 'FBK-MS':
        return 0.419907 * ( 1. - math.exp(-1.*0.3046*ov) )
    # -- new cell size --
    elif type == 'HPK-ES2-20um':
        return 0.576 * ( 1. - math.exp(-1.*0.625*ov) )
    elif type == 'HPK-ES2-25um':
        return 0.638 * ( 1. - math.exp(-1.*0.651*ov) )
    elif type == 'HPK-ES2-30um':
        return 0.653 * ( 1. - math.exp(-1.*0.728*ov) )
    # -- low Cg --
    elif type == 'HPK-ES3-20um':
        return 0.568 * ( 1. - math.exp(-1.*0.588*ov) )
    elif type == 'HPK-ES3-25um':
        return 0.638 * ( 1. - math.exp(-1.*0.589*ov) )
    else:
        print 'CANNOT FIND PDE'
