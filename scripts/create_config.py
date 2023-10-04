#!/usr/bin/env python

#--------> ex: python create_config.py -r 66448-66461 -t 12 -ov 1.5 -ml HPK_nonIrr_C25_LYSO813 -c config_23.00

import os, re
import commands
import math, time
import sys
import argparse
import subprocess

# ----
cfgFolder = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/cfg'
# ----


parser = argparse.ArgumentParser(description='This script creates moduleCharacterization cfg and minEnergy')

parser.add_argument("-ml",  "--modulelabel",     required=True,  type=str, help="module label")
parser.add_argument("-r",  "--runs",             required=True,  type=str, help="comma-separated list of runs to be processed")
parser.add_argument("-t",  "--temperature",      required=True,  type=str, help="temperature")
parser.add_argument("-ov", "--Vov",              required=True,  type=str, help="overvoltage")
parser.add_argument("-c",  "--config",             required=True,  type=str, help="config number")
parser.add_argument("-e", "--extraLabel",    required=False, type=str, help="eg: angle or check or whatever")

args = parser.parse_args()
runs = args.runs

if args.extraLabel:
   label = '%s_Vov%.2f_%s_T%sC' %(args.modulelabel, float(args.Vov),args.extraLabel,  args.temperature)
   module_label = "%s_%s"%(args.modulelabel,args.extraLabel)
else:
   label = '%s_Vov%.2f_T%sC' %(args.modulelabel, float(args.Vov) , args.temperature)
   module_label = "%s"%args.modulelabel 


#---- write min energy ---

temp_min = '%s/minEnergies_%s.txt'%(cfgFolder,args.modulelabel)
if not (os.path.isfile(temp_min)):
   baseMinEnergy = open('%s/minEnergies_base.txt'%cfgFolder, 'r')
   newMinEnergy = open('%s/minEnergies_%s.txt'%(cfgFolder,args.modulelabel), 'w')

   command = 'cp %s/minEnergies_base.txt %s/minEnergies_%s.txt'%(cfgFolder, cfgFolder, args.modulelabel)
   os.system(command)

# create the extra label min energy
if args.extraLabel:
   temp_min = '%s/minEnergies_%s_%s.txt'%(cfgFolder,args.modulelabel,args.extraLabel)
   if not (os.path.isfile(temp_min)):
      baseMinEnergy = open('%s/minEnergies_%s.txt'%(cfgFolder,args.modulelabel), 'r')
      newMinEnergy = open('%s/minEnergies_%s_%s.txt'%(cfgFolder,args.modulelabel,args.extraLabel), 'w')

      command = 'cp %s/minEnergies_%s.txt %s/minEnergies_%s_%s.txt'%(cfgFolder,args.modulelabel, cfgFolder, args.modulelabel,args.extraLabel)
      os.system(command)
      



# --- write cfg ---- moduleChar
baseCfg = open('%s/moduleCharacterization_base.cfg'%cfgFolder, 'r')

if args.extraLabel:
   newCfg = open('%s/moduleCharacterization_%s.cfg'%(cfgFolder,label), 'w')
   print 'writing \t moduleCharacterization_%s.cfg'%(label)
else:
   newCfg = open('%s/moduleCharacterization_%s.cfg'%(cfgFolder,label), 'w')
   print 'writing \t moduleCharacterization_%s.cfg'%(label)

for line in baseCfg:
   if (line.startswith('Vov') and args.Vov not in line):
      print '\n---------------- \n ERROR: missing ov in moduleCharacterization.cfg file\n'
      newCfg.write(line + '%s \n'%args.Vov) # non funziona perche va a capo
      sys.exit()
   elif 'runNumbers' in line:
      newCfg.write(line.replace('runNumbers', '%s'%runs))
   elif 'generalLabel' in line:
      newCfg.write(line.replace('generalLabel', '%s'%label))
   elif 'moduleLabel' in line:
      newCfg.write(line.replace('moduleLabel', '%s'%module_label))
   elif 'confNumber' in line:
      newCfg.write(line.replace('confNumber', '%s'%args.config))
      print 'config : ', args.config

   elif 'vovLabel' in line:
      newCfg.write(line.replace('vovLabel', '%s'%args.Vov))
   else:
      newCfg.write(line)


baseCfg.close()
newCfg.close()



# --- write cfg ---- pulseShape
baseCfg = open('%s/drawPulseShapeTB_base.cfg'%cfgFolder, 'r')


if args.extraLabel:
   newCfg = open('%s/drawPulseShapeTB_%s.cfg'%(cfgFolder,label), 'w')
   print 'writing \t drawPulseShapeTB_%s.cfg'%(label)
else:
   newCfg = open('%s/drawPulseShapeTB_%s.cfg'%(cfgFolder,label), 'w')
   print 'writing \t drawPulseShapeTB_%s.cfg'%(label)


for line in baseCfg:
   if (line.startswith('Vov') and args.Vov not in line):
      newCfg.write(line + '%s'%args.Vov)
   elif 'runNumbers' in line:
      newCfg.write(line.replace('runNumbers', '%s'%runs))
   elif 'generalLabel' in line:
      newCfg.write(line.replace('generalLabel', '%s'%label))
   elif 'moduleLabel' in line:
      newCfg.write(line.replace('moduleLabel', '%s'%module_label))
   elif 'confNumber' in line:
      newCfg.write(line.replace('confNumber', '%s'%args.config))
      print 'config : ', args.config
   elif 'vovLabel' in line:
      newCfg.write(line.replace('vovLabel', '%s'%args.Vov))


   else:
      newCfg.write(line)

baseCfg.close()
newCfg.close()




