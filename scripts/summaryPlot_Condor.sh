#!/bin/bash
#!/bin/sh
echo
echo 'START---------------'
echo 'current dir: ' ${PWD}
cd /afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/
source scripts/setup.sh
cd /afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/macros
echo 'current dir: ' ${PWD}
python moduleCharacterizationSummaryPlots.py -m 2 -i $1 -o $2
echo 'STOP---------------'
echo
echo
