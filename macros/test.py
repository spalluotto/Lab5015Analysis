from energy_scaling import *

aa = 3.75
aa = [3.75, 3, 2.4, 4.2]

for a in aa:
    print(a)
    energy_vs_eta(thickness=a)
    e = eta_from_alpha(32, t=a)
    print("---",e)
