# Creating a list of filenames
filenames = [
    'list_cfg_moduleCharacterization_LYSO815.txt',
    'list_cfg_moduleCharacterization_LYSO100056.txt'
]

outfile = 'mergedfiles_moduleCharacterization.txt'

 
# Open file3 in write mode
with open('%s'%outfile, 'w') as outfile:
 
    # Iterate through list
    for names in filenames:
 
        # Open each file in read mode
        with open(names) as infile:
 
            # read the data from file1 and
            # file2 and write it in file3
            outfile.write(infile.read())
 
        # Add '\n' to enter data of file2
        # from next line
        outfile.write("\n")


print 'output file : ', outfile
