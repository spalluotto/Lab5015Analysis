cd /afs/cern.ch/user/s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/
source scripts/setup.sh
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov3.50.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov3.50.cfg

./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_T12C_Vov3.50_angle32_check.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_T12C_Vov3.50_angle32_check.cfg

./bin/drawPulseShapeTB.exe cfg/drawPulseShapeTB_HPK_nonIrr_C25_LYSO813_Vov3.50.cfg
