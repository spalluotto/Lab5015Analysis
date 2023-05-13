#!/bin/bash
#!/bin/sh
echo
echo 'START---------------'
echo 'current dir: ' ${PWD}
cd /afs/cern.ch/user/s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/
echo 'current dir: ' ${PWD}
source scripts/setup.sh
./bin/drawPulseShapeTB.exe $1
echo 'STOP---------------'
echo
echo
