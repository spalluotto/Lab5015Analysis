# Creating a list of filenames
filenames = [
    'list_cfg_drawPulseShapeTB_LYSO100056.txt',
    'list_cfg_drawPulseShapeTB_LYSO200104.txt',
    'list_cfg_drawPulseShapeTB_LYSO300032.txt',
    'list_cfg_drawPulseShapeTB_LYSO813.txt',
    'list_cfg_drawPulseShapeTB_LYSO815.txt',
    'list_cfg_drawPulseShapeTB_LYSO816.txt',
    'list_cfg_drawPulseShapeTB_LYSO818.txt',
    'list_cfg_drawPulseShapeTB_LYSO819.txt',
    'list_cfg_drawPulseShapeTB_LYSO820.txt',
    'list_cfg_drawPulseShapeTB_LYSO825.txt',
    'list_cfg_drawPulseShapeTB_LYSO528.txt'
]

outfile = 'mergedfiles_drawPulseShapeTB.txt'

 
with open('%s'%outfile, 'w') as outfile:
    for names in filenames:
        with open(names) as infile:
            outfile.write(infile.read())
        outfile.write("\n")
print('output file : ', outfile)
