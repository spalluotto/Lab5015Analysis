import subprocess

directory_path = "/path/to/search"
desired_date = "2023-01-01"  # Format: YYYY-MM-DD

# Construct the find command
find_command = [
    "find",
    directory_path,
    "-type",
    "f",
    "-newermt",
    desired_date,
    "!",
    "-newermt",
    desired_date + " 23:59:59",  # End of the day
    "-exec",
    "rm",
    "{}",
    ";"
]

# Execute the find command
try:
    subprocess.run(find_command, check=True)
    print("Files deleted successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
