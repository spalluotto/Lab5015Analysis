cd /afs/cern.ch/user/s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/
source scripts/setup.sh

./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov0.50.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov0.80.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov1.50.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov3.50.cfg


./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov0.50.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov0.80.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov1.50.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov3.50.cfg

cd /afs/cern.ch/user/s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/macros

python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO816_T12C_Vov0.50 -o HPK_nonIrr_C25_LYSO816_T12C_Vov0.50
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO816_T12C_Vov0.80 -o HPK_nonIrr_C25_LYSO816_T12C_Vov0.80
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO816_T12C_Vov1.50 -o HPK_nonIrr_C25_LYSO816_T12C_Vov1.50
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO816_T12C_Vov3.50 -o HPK_nonIrr_C25_LYSO816_T12C_Vov3.50

python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO816_T12C_Vov0.50,HPK_nonIrr_C25_LYSO816_T12C_Vov0.80,HPK_nonIrr_C25_LYSO816_T12C_Vov1.50,HPK_nonIrr_C25_LYSO816_T12C_Vov3.50 -o HPK_nonIrr_C25_LYSO816_T12C
