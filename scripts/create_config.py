#!/usr/bin/env python

#--------> ex: python create_config.py -r 66448-66461 -t 12 -ov 1.5 -ml HPK_nonIrr_C15_LYSO528 -d config_run66353

import os, re
import commands
import math, time
import sys
import argparse
import subprocess

# ----
cfgFolder = '/afs/cern.ch/user/s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/cfg'
# ----


parser = argparse.ArgumentParser(description='This script creates moduleCharacterization cfg and minEnergy')

parser.add_argument("-ml",  "--modulelabel",     required=True,  type=str, help="module label")
parser.add_argument("-r",  "--runs",             required=True,  type=str, help="comma-separated list of runs to be processed")
parser.add_argument("-t",  "--temperature",      required=True,  type=str, help="temperature")
parser.add_argument("-ov", "--Vov",              required=True,  type=str, help="overvoltage")
parser.add_argument("-d",  "--disc",             required=False,  type=str, help="disc calibration config")
parser.add_argument("-e", "--extraLabel",    required=False, type=str, help="eg: angle or check or whatever")

args = parser.parse_args()

runs = args.runs

if args.extraLabel:
   label = '%s_T%sC_Vov%.2f_%s' %(args.modulelabel, args.temperature, float(args.Vov),args.extraLabel)
else:
   label = '%s_T%sC_Vov%.2f' %(args.modulelabel, args.temperature, float(args.Vov))


#---- write min energy ---

temp_min = '%s/minEnergies_%s.txt'%(cfgFolder,args.modulelabel)
if not (os.path.isfile(temp_min)):
   baseMinEnergy = open('%s/minEnergies_base.txt'%cfgFolder, 'r')
   newMinEnergy = open('%s/minEnergies_%s.txt'%(cfgFolder,args.modulelabel), 'w')

   command = 'cp %s/minEnergies_base.txt %s/minEnergies_%s.txt'%(cfgFolder, cfgFolder, args.modulelabel)

   os.system(command)

# --- write cfg ---- moduleChar
baseCfg = open('%s/moduleCharacterization_base.cfg'%cfgFolder, 'r')

if args.extraLabel:
   newCfg = open('%s/moduleCharacterization_%s_Vov%.2f_%s.cfg'%(cfgFolder,args.modulelabel,float(args.Vov),args.extraLabel), 'w')
   print 'writing \t moduleCharacterization_%s_Vov%.2f_%s.cfg'%(args.modulelabel,float(args.Vov),args.extraLabel)
else:
   newCfg = open('%s/moduleCharacterization_%s_Vov%.2f.cfg'%(cfgFolder,args.modulelabel,float(args.Vov)), 'w')
   print 'writing \t moduleCharacterization_%s_Vov%.2f.cfg'%(args.modulelabel,float(args.Vov))

for line in baseCfg:
   if (line.startswith('Vov') and args.Vov not in line):
      newCfg.write(line + '%s'%args.Vov)
   elif 'runNumbers' in line:
      newCfg.write(line.replace('runNumbers', '%s'%runs))
   elif 'generalLabel' in line:
      newCfg.write(line.replace('generalLabel', '%s'%label))
   elif 'moduleLabel' in line:
      newCfg.write(line.replace('moduleLabel', '%s'%args.modulelabel))


   else:
      if args.disc and 'disc_config' in line:
         newCfg.write(line.replace('disc_config', '%s'%args.disc))
         print 'disc calib: ', args.disc

      else:
         newCfg.write(line)

baseCfg.close()
newCfg.close()



# --- write cfg ---- pulseShape
baseCfg = open('%s/drawPulseShapeTB_base.cfg'%cfgFolder, 'r')

if args.extraLabel:
   newCfg = open('%s/drawPulseShapeTB_%s_Vov%.2f_%s.cfg'%(cfgFolder,args.modulelabel,float(args.Vov),args.extraLabel), 'w')
   print 'writing \t drawPulseShapeTB_%s_Vov%.2f_%s.cfg'%(args.modulelabel,float(args.Vov),args.extraLabel)
else:
   newCfg = open('%s/drawPulseShapeTB_%s_Vov%.2f.cfg'%(cfgFolder,args.modulelabel,float(args.Vov)), 'w')
   print 'writing \t drawPulseShapeTB_%s_Vov%.2f.cfg'%(args.modulelabel,float(args.Vov))

for line in baseCfg:
   if (line.startswith('Vov') and args.Vov not in line):
      newCfg.write(line + '%s'%args.Vov)
   elif 'runNumbers' in line:
      newCfg.write(line.replace('runNumbers', '%s'%runs))
   elif 'generalLabel' in line:
      newCfg.write(line.replace('generalLabel', '%s'%label))
   elif 'moduleLabel' in line:
      newCfg.write(line.replace('moduleLabel', '%s'%args.modulelabel))


   else:
      if args.disc and 'disc_config' in line:
         newCfg.write(line.replace('disc_config', '%s'%args.disc))
         print 'disc calib: ', args.disc

      else:
         newCfg.write(line)

baseCfg.close()
newCfg.close()




