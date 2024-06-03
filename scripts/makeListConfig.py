#!/usr/bin/env python
import os, sys
import re

outFolder = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/scripts/'

cfgFolder = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/cfg/'
path = cfgFolder

txtName = 'list_cfg_moduleCharacterization_LYSO'
txtPSName = 'list_cfg_drawPulseShapeTB_LYSO'

outFiles = {}
outFilesPS = {}


if outFolder[-1] != "/": outFolder += '/'

for path_, subdirs, files in os.walk(path):
    for name in files:
        if not (name.startswith("moduleCharacterization") or name.startswith("drawPulseShapeTB")): continue
        if not name.endswith('.cfg'): continue        
        if 'LYSO' not in name:
            print('cannot find LYSO ID for ', name)
            continue
        print('\n\nname: ', name)
        moduleNum = re.search(r'LYSO(\d{3}|\d{6})_', name).group(1)  # look for the three numbers after "LYSO"
        if name.startswith("moduleCharacterization"):
            if moduleNum not in outFiles:
                print('module ID: ', moduleNum)
                outFiles[moduleNum] = open('%s/%s%s.txt'%(outFolder,txtName,str(moduleNum)),'w')        
            outFiles[moduleNum].writelines('%s\n'%os.path.join(path_, name))
        elif name.startswith("drawPulseShapeTB"):
            if moduleNum not in outFilesPS:
                print('module ID: ', moduleNum)
                outFilesPS[moduleNum] = open('%s/%s%s.txt'%(outFolder,txtPSName,str(moduleNum)),'w')        
            outFilesPS[moduleNum].writelines('%s\n'%os.path.join(path_, name))
        else:
            continue


#---- counter -----
print('\n ModuleChar')
for outFile in outFiles:
    outFiles[outFile].close()
    with open('%s/%s%s.txt'%(outFolder,txtName,outFile),'r') as fp:
        for count, line in enumerate(fp):
            pass
    print('\n\tmodule:  ', outFile, '\tn n cfg files: ', count+1)

#----
print('\n Pulse Shape')
for outFile in outFilesPS:
    outFilesPS[outFile].close()
    with open('%s/%s%s.txt'%(outFolder,txtPSName,outFile),'r') as fp:
        for count, line in enumerate(fp):
            pass
    print('\n\tmodule:  ', outFile, '\tn n cfg files: ', count+1)



