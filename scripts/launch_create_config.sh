# usage: create_config.py [-h] -ml MODULELABEL -r RUNS -t TEMPERATURE -ov VOV -c CONFIG -th THRESHOLD [-vvth1 THRESHOLDT1] [-vth2 THRESHOLDT2] [-vthe THRESHOLDE] [-e EXTRALABEL]
#                         [--whichEnergyIntercalib WHICHENERGYINTERCALIB] [--dutASIC DUTASIC] [--refASIC REFASIC] [--refBar REFBAR] [--calibBar CALIBBAR] [--saveRefInfoFlag SAVEREFINFOFLAG]
#                         [--refCalibPath REFCALIBPATH] [--refAmpWalkPerBar REFAMPWALKPERBAR]

# python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR --refBar 6  --calibBar 8  -e positionScan
# python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR --refBar 7  --calibBar 8  -e positionScan
# python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR --refBar 8  --calibBar 8  -e positionScan
# python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR --refBar 9  --calibBar 8  -e positionScan
# python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR --refBar 10 --calibBar 8  -e positionScan

python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR_LO --refBar 6  --calibBar 8  -e positionScan
python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR_LO --refBar 7  --calibBar 8  -e positionScan
python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR_LO --refBar 8  --calibBar 8  -e positionScan
python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR_LO --refBar 9  --calibBar 8  -e positionScan
python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR_LO --refBar 10 --calibBar 8  -e positionScan

# python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR_LO --refBar 6  --calibBar 8  -e positionScan_PDEGaincor
# python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR_LO --refBar 7  --calibBar 8  -e positionScan_PDEGaincor
# python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR_LO --refBar 8  --calibBar 8  -e positionScan_PDEGaincor
# python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR_LO --refBar 9  --calibBar 8  -e positionScan_PDEGaincor
# python3 create_config.py -t 18    -th vth1     -ml DM_FE_4587 -c config_88.00 -ov 3 -r 4281 --whichEnergyIntercalib TOFHIR_LO --refBar 10 --calibBar 8  -e positionScan_PDEGaincor
