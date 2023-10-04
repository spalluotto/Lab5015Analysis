import re

input_launcher = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/scripts/launch_create_config.sh'
list_outfile = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/scripts/list_summaryPlot.txt'
launcher =  '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/macros/launch_summaryPlot.sh'
summary = '/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/macros/launch_sum_summary.sh'


# Create a dictionary to store lines grouped by common arguments (excluding "ov")  --> for summary of summaries
grouped_lines = {}

# Open the input and output files
with open(input_launcher, 'r') as input_file, open(list_outfile, 'w') as output_file, open(launcher, 'w') as launcher_file:
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
            new_line = '{}_Vov{:.2f}_{}_T{}C {}_Vov{:.2f}_{}_T{}C\n'.format(module_label, ov, extra_label, temp, module_label, ov, extra_label, temp)
            new_line_launcher = 'python moduleCharacterizationSummaryPlots.py -m 2 -i {}_Vov{:.2f}_{}_T{}C -o {}_Vov{:.2f}_{}_T{}C\n'.format(module_label, ov, extra_label, temp, module_label, ov, extra_label, temp)

            # Write the new command to the output file
            output_file.write(new_line)

            launcher_file.write(new_line_launcher)



            # Create a key for the dictionary excluding "ov" value ---> for the summary of summaries
            key = (module_label, temp, extra_label)
            if key not in grouped_lines:
                grouped_lines[key] = []
            grouped_lines[key].append(ov)

            print('\n',key)



print('\n\nECCO QUI :')
for key in grouped_lines:
    print('\n KEY: ', key, '    --->    OVs:   ', grouped_lines[key])
    

# Write the grouped lines to the output file
with open(summary, 'w') as sum_file:
    for key, ov_values in grouped_lines.items():
        module_label, temp, extra_label = key
        ov_values = sorted(ov_values)  # Sort "ov" values
        start = '{}'.format(module_label)
        end = '{}_T{}C'.format(extra_label,temp)
        sum_line = ''
        for it,ov in enumerate(ov_values):
            if it != 0:
                sum_line += ','
            sum_line += '{}_Vov{:.2f}_{}'.format(start,ov,end)
    
        new_line_sum = 'python moduleCharacterizationSummaryPlots.py -m 2 -i {} -o {}_{}\n\n'.format(sum_line,start,end)
        sum_file.write(new_line_sum)
