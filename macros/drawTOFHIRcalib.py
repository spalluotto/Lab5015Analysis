from calibration_utils import *

eos_www = "/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep25/energy_intercalibration/"

# input_labels = ["DM_9001_Vov3.00_T18C", "DM_9001_Vov2.00_T18C", "DM_9001_Vov1.20_T18C", "DM_9001_Vov0.90_T18C"]
# input_labels = ["DM_9005_Vov3.00_T18C","DM_9005_Vov2.00_T18C"]
# input_labels = ["DM_9000_Vov3.00_T18C","DM_9000_Vov2.00_T18C"]

input_labels = ["DM_348_Vov3.00_T18C_conf83_refBar8", "DM_348_Vov3.00_T18C_conf84_refBar8", "DM_348_Vov3.00_T18C_conf87_refBar9", "DM_348_Vov3.00_T18C_conf88_refBar8", "DM_348_Vov3.00_T18C_conf93_refBar8"]
labels = ["conf83", "conf84", "conf87", "conf88","conf93"]
out_label = "conf83_84_87_88_93"

csv_files = [f"{eos_www}{label}/TOFHIR_calibration_factors.csv" for label in input_labels]

#plot_TOFHIR_calibration_multi(csv_files)
plot_calibrations(csv_files, out_label, ylim=(0.5, 2.0),labels=labels)
