from calibration_utils import *
modules_list = ["32110020000691", "32110020000800", "32110020001006", "32110020001220", "32110020001365", "32110020002158", "32110020004413", "32110020004436", "32110020004955"]
for module in modules_list:
    plot_LO_calibration(f"/eos/home-s/spalluot/MTD/TB_CERN_Sep25/Lab5015Analysis/plots/module_{module}_LO_calibration_factors.csv")
