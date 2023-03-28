cd /afs/cern.ch/user/s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/
source scripts/setup.sh

# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov0.50.cfg
# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov0.50_angle64.cfg
# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov0.80.cfg
# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov0.80_angle64.cfg
# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov1.00.cfg
# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov1.50.cfg
# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov1.50_angle64.cfg
# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov2.00.cfg
# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov3.50.cfg
# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov3.50_angle64.cfg


# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov0.50.cfg
# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov0.50_angle64.cfg
# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov0.80.cfg
# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov0.80_angle64.cfg
# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov1.00.cfg
# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov1.50.cfg
# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov1.50_angle64.cfg
# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov2.00.cfg
# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov3.50.cfg
# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO813_Vov3.50_angle64.cfg


# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov0.50.cfg
# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov0.80.cfg
# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov1.50.cfg
# ./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov3.50.cfg


# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov0.50.cfg
# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov0.80.cfg
# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov1.50.cfg
# ./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO816_Vov3.50.cfg


cd macros

python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO813_T12C_Vov0.50 -o HPK_nonIrr_C25_LYSO813_T12C_Vov0.50
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO813_T12C_Vov0.80 -o HPK_nonIrr_C25_LYSO813_T12C_Vov0.80
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO813_T12C_Vov1.50 -o HPK_nonIrr_C25_LYSO813_T12C_Vov1.50
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO813_T12C_Vov2.00 -o HPK_nonIrr_C25_LYSO813_T12C_Vov2.00
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO813_T12C_Vov3.50 -o HPK_nonIrr_C25_LYSO813_T12C_Vov3.50

python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO816_T12C_Vov0.50 -o HPK_nonIrr_C25_LYSO816_T12C_Vov0.50
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO816_T12C_Vov0.80 -o HPK_nonIrr_C25_LYSO816_T12C_Vov0.80
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO816_T12C_Vov1.50 -o HPK_nonIrr_C25_LYSO816_T12C_Vov1.50
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO816_T12C_Vov3.50 -o HPK_nonIrr_C25_LYSO816_T12C_Vov3.50


python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO813_T12C_Vov0.50,HPK_nonIrr_C25_LYSO813_T12C_Vov0.80,HPK_nonIrr_C25_LYSO813_T12C_Vov1.50,HPK_nonIrr_C25_LYSO813_T12C_Vov2.00,HPK_nonIrr_C25_LYSO813_T12C_Vov3.50 -o HPK_nonIrr_C25_LYSO813_T12C


python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO816_T12C_Vov0.50,HPK_nonIrr_C25_LYSO816_T12C_Vov0.80,HPK_nonIrr_C25_LYSO816_T12C_Vov1.50,HPK_nonIrr_C25_LYSO816_T12C_Vov3.50 -o HPK_nonIrr_C25_LYSO816_T12C

cd ..

./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov0.50.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov0.80.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov1.50.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov3.50.cfg

./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov0.50.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov0.80.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov1.50.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov3.50.cfg

cd macros

python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO818_T12C_Vov0.50 -o HPK_nonIrr_C25_LYSO818_T12C_Vov0.50
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO818_T12C_Vov0.80 -o HPK_nonIrr_C25_LYSO818_T12C_Vov0.80
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO818_T12C_Vov1.50 -o HPK_nonIrr_C25_LYSO818_T12C_Vov1.50
python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO818_T12C_Vov3.50 -o HPK_nonIrr_C25_LYSO818_T12C_Vov3.50

python moduleCharacterizationSummaryPlots.py -m 2 -i HPK_nonIrr_C25_LYSO818_T12C_Vov0.50,HPK_nonIrr_C25_LYSO818_T12C_Vov0.80,HPK_nonIrr_C25_LYSO818_T12C_Vov1.50,HPK_nonIrr_C25_LYSO818_T12C_Vov3.50 -o HPK_nonIrr_C25_LYSO818_T12C

cd ..

./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov0.50_angle32.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov0.50_angle64.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov0.80_angle32.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov0.80_angle64.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov1.50_angle32.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov1.50_angle64.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov3.50_angle32.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov3.50_angle32_check.cfg
./bin/moduleCharacterization_step1.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov3.50_angle64.cfg

./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov0.50_angle32.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov0.50_angle64.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov0.80_angle32.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov0.80_angle64.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov1.50_angle32.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov1.50_angle64.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov3.50_angle32.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov3.50_angle32_check.cfg
./bin/moduleCharacterization_step2.exe cfg/moduleCharacterization_HPK_nonIrr_C25_LYSO818_Vov3.50_angle64.cfg


