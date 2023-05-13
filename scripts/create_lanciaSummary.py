#!/usr/bin/env python
import os, sys
import re

command_base = 'python moduleCharacterizationSummaryPlots.py -m 2'

outFolder = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/macros/'

plotFolder = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/'
path = plotFolder

txtName = 'lanciaSummaryPlots.sh'

if outFolder[-1] != "/": outFolder += '/'

for path_, subdirs, files in os.walk(path):
    for name in files:
        if not name.startswith("moduleCharacterization_step1"): continue
        if not name.endswith('.root'): continue        
        if 'LYSO' not in name:
            print 'cannot find LYSO ID for ', name
            continue

        print '\n\nname: ', name
        label = name.split("moduleCharacterization_step1_")[1].split(".root")[0]


        # write in the txt file
        add = '%s -i %s -o %s'%(command_base,label, label)
        outFiles = open('%s/%s'%(outFolder,txtName), 'a')
        outFiles.write('%s\n'%add)


        print '%s   \n'%add

outFiles.write('\n\n')
outFiles.close()


