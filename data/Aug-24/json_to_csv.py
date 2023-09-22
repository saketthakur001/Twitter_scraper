import json
import os

# Get the current working directory
directory_path = os.getcwd()
merged_data = []

# Iterate through all the files in the directory
for file_name in os.listdir(directory_path):
    if file_name.endswith(".json"):
        file_path = os.path.join(directory_path, file_name)
        
        with open(file_path, 'r') as file:
            data = json.load(file)
            merged_data.append(data)

# # Write the merged data to a new file
# with open("merged_file.json", 'w') as file:
#     json.dump(merged_data, file, indent=4)
