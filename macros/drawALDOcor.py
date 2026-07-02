import json
import math
import numpy as np
import matplotlib.pyplot as plt

def PDE(ov):
    return 0.638 * (1.0 - math.exp(-0.651 * ov))

def Gain(ov):
    return 7.044E04 + 2.895E05 * ov

def Signal(ov):
    return PDE(ov) * Gain(ov)

def plotPDExGain(sm_id, ov_set, json_file="/eos/home-s/spalluot/MTD/TB_CERN_Sep25/Lab5015Analysis/plots/ALDOcor.json"):
    with open(json_file, "r") as f:
        data = json.load(f)
    row = None
    for r in data:
        if r["id"] == sm_id and float(r["ovSet"]) == float(ov_set):
            row = r
            break
    if row is None:
        raise ValueError(f"[ERROR] No match for id={sm_id}, ov={ov_set}")

    # corrected OV values
    ovL = row["ov0corr"]
    ovR = row["ov1corr"]

    vov = np.linspace(0, 4.0, 500)
    sig = [Signal(v) for v in vov]
    sig_nom = Signal(ov_set)
    sigL = Signal(ovL)
    sigR = Signal(ovR)
    asym = 100.0 * (sigL - sigR) / sig_nom
    plt.figure(figsize=(7,5))
    plt.plot(vov, sig, color="black", lw=2, label=r"PDE $\times$ Gain")
    plt.axvline(ov_set, color="black", linestyle="--", alpha=0.7, label=f"Nominal OV = {ov_set:.1f} V")    
    plt.scatter(ovL, sigL, color="red", s=100, zorder=10, label=f"Left = {ovL:.2f} V")
    plt.scatter(ovR, sigR, color="blue", s=100, zorder=10, label=f"Right = {ovR:.2f} V")
    plt.xlabel(r"$V_{OV}$ [V]")
    plt.ylabel(r"PDE $\times$ Gain")
    plt.title(f"SM {sm_id}")
    plt.text( 0.05, 0.95, f"Asymmetry = {asym:.1f}%", transform=plt.gca().transAxes, verticalalignment="top" )
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("test.png")

plotPDExGain("32110020004436", 3)
