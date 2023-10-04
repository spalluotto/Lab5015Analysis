import os


folder_path = "/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/"
output_file = "faulty_files.txt"
target_size = 1000


# Function to list files with size smaller than target size
def list_faulty_files(folder_path):
    faulty_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".root"):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                if file_size < target_size:
                    faulty_files.append(file)
    return faulty_files


faulty_files_list = list_faulty_files(folder_path)

with open(output_file, 'w') as file:
    file.write("\n".join(faulty_files_list))
