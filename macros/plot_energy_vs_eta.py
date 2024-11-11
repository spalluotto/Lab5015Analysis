#! /usr/bin/env python
from utils import *

# --- EDIT ---
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/energy_studies/'
verbose = False
xmax = 1.65
stochPow = 0.73
T1 = 3.75
Fcorr = 3.7/(0.86*T1)
thick = T1*Fcorr
angles = [32,52,64]
# ---------


# draw graphs
g_e_vs_eta = energy_vs_eta(plot_name=f"{outdir}/c_energy_vs_eta_T1.png",thickness=T1)
g_e_vs_eta_thick = energy_vs_eta(plot_name=f"{outdir}/c_energy_vs_eta_thickCorr.png",thickness=thick)
g_e_vs_beta = energy_vs_alpha(plot_name=f"{outdir}/c_energy_vs_angleTB_T1.png",thickness=T1)
g_e_vs_beta_thick = energy_vs_alpha(plot_name=f"{outdir}/c_energy_vs_angleTB_thickCorr.png",thickness=thick)

etaMap = {}
etaMap_corr = {}
for angle in angles:
    print("\nTHICKNESS: ", T1)
    etaMap[angle] = eta_from_alpha(angle, t=T1)

    print("\nTHICKNESS: ", thick)
    etaMap_corr[angle] = eta_from_alpha(angle, t=thick)

print("non corr ", etaMap)
print("corr ", etaMap_corr)

fit_simulation(g_e_vs_eta_sim, plot_name=f"{outdir}/c_energy_vs_eta_simulation.png")
