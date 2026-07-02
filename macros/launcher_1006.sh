# # --- TOFHIR calibrations ---
#python3 writeTOFHIRcalib.py -i DM_9000_Vov3.00_T18C -o DM_9000_Vov3.00_T18C -sm 32110020001006 --minEnergy DM_9000 --drawCalib --drawComparison --fitCheck --drawMPVvsBar
# python3 writeTOFHIRcalib.py -i DM_9000_Vov2.00_T18C -o DM_9000_Vov2.00_T18C -sm 32110020001006 --minEnergy DM_9000 --drawCalib --drawComparison --fitCheck --drawMPVvsBar

# ---- compare Landau spectra in bad and good bars -------
# python3 draw_energy.py -b 11,9  -i DM_9000_Vov3.00_T18C
# python3 draw_energy.py -b 11,9  -i DM_9000_Vov3.00_T18C_TOFHIRcalib
# python3 draw_energy.py -b 11,9  -i DM_9000_Vov3.00_T18C_TOFHIR_LOcalib

# # ---- ER studies vs bar -----
# python3 draw_LandauPars_vs_pos.py --minEnergy DM_9000   -i DM_9000_Vov3.00_T18C
# python3 draw_LandauPars_vs_pos.py --minEnergy DM_9000   -i DM_9000_Vov2.00_T18C

# python3 draw_LandauPars_vs_pos.py --minEnergy DM_9000   -i DM_9000_Vov3.00_T18C_TOFHIRcalib
# python3 draw_LandauPars_vs_pos.py --minEnergy DM_9000   -i DM_9000_Vov2.00_T18C_TOFHIRcalib

# python3 draw_LandauPars_vs_pos.py --minEnergy DM_9000   -i DM_9000_Vov3.00_T18C_TOFHIR_LOcalib
# python3 draw_LandauPars_vs_pos.py --minEnergy DM_9000   -i DM_9000_Vov2.00_T18C_TOFHIR_LOcalib

# # ---- ER studies vs impact position -----
python3 draw_LandauPars_vs_pos.py --minEnergy DM_9000  -i DM_9000_Vov3.00_T18C_refBar6_TOFHIR_LOcalib,DM_9000_Vov3.00_T18C_refBar7_TOFHIR_LOcalib,DM_9000_Vov3.00_T18C_refBar8_TOFHIR_LOcalib,DM_9000_Vov3.00_T18C_refBar9_TOFHIR_LOcalib,DM_9000_Vov3.00_T18C_refBar10_TOFHIR_LOcalib -o DM_9000_Vov3.00_T18C_refBar6to10_TOFHIR_LOcalib

# ----- draw landau pars vs vov -------
# python3 draw_LandauPars_vs_vov.py --minEnergy DM_9000 -i DM_9000_Vov2.00_T18C_TOFHIR_LOcalib,DM_9000_Vov3.00_T18C_TOFHIR_LOcalib -o DM_9000_Vovs_T18C_TOFHIR_LOcalib

# ----- ER correlations ----------- this requires summaryPlots
# python3 correlate_ER.py -sm 32110020001006 --minEnergy DM_9000 --extraLabel calib  -i DM_9000_Vov3.00_T18C_TOFHIR_LOcalib
# python3 correlate_ER.py -sm 32110020001006 --minEnergy DM_9000 --extraLabel calib  -i DM_9000_Vov2.00_T18C_TOFHIR_LOcalib

# ----- tres vs impact position -----------
#python3 draw_tres_vs_pos.py -th 10  -i DM_9000_Vov3.00_T18C_refBar6_TOFHIR_LOcalib,DM_9000_Vov3.00_T18C_refBar7_TOFHIR_LOcalib,DM_9000_Vov3.00_T18C_refBar8_TOFHIR_LOcalib,DM_9000_Vov3.00_T18C_refBar9_TOFHIR_LOcalib,DM_9000_Vov3.00_T18C_refBar10_TOFHIR_LOcalib -o DM_9000_Vov3.00_T18C_refBar6to10_tres_TOFHIR_LOcalib
