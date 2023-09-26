import re

input_launcher = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/scripts/launch_create_config.sh'
outfile = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/macros/launch_summaryPlots.sh'


# Open the input and output files
with open(input_launcher, 'r') as input_file, open(outfile, 'w') as output_file:
    # Iterate through each line in the input file
    for line in input_file:
        if not line.startswith('python create_config.py'):
            continue

        # Use regular expressions to extract the required information
        matches = re.findall(r'-([a-zA-Z]+)\s+([^\s]+)', line)  # Find all argument-value pairs

        # Initialize variables for the argument values
        temp = None
        module_label = None
        config = None
        extra_label = None
        ov = None
        run = None

        # Process the argument-value pairs
        for match in matches:
            arg, value = match
            if arg == 't':
                temp = value
            elif arg == 'ml':
                module_label = value
            elif arg == 'c':
                config = value
            elif arg == 'e':
                extra_label = value
            elif arg == 'ov':
                ov = float(value)
            elif arg == 'r':
                run = value


        print(module_label)

        if temp and module_label and config and extra_label and ov and run:
            # Create the new command
            new_line = 'python moduleCharacterizationSummaryPlots.py -m 2 -i {}_Vov{:.2f}_{}_T{}C -o {}_Vov{:.2f}_{}_T{}C\n'.format(module_label, ov, extra_label, temp, module_label, ov, extra_label, temp)

            # Write the new command to the output file
            output_file.write(new_line)
