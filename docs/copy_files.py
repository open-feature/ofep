import os
import shutil

# Get the root directory of the repository
root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Define the source and destination directories
source_directory = os.path.join(root_directory, 'OFEP')
destination_directory = os.path.join(root_directory, 'docs', 'source')
source_subdirectory = os.path.join(source_directory, 'images')
destination_subdirectory = os.path.join(destination_directory, 'images')

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# Copy the ofeps from OFEP directory to docs/source
for filename in os.listdir(source_directory):
    if filename.endswith('.md') and filename.find('template')==-1 and filename.find('index')==-1:
        source_file_path = os.path.join(source_directory, filename)
        destination_file_path = os.path.join(destination_directory, filename)
        if os.path.exists(destination_file_path):
            os.remove(destination_file_path)
        shutil.copy2(source_file_path, destination_file_path)
        print(f"Copied {source_file_path} to {destination_file_path}")

print("Copying completed.")


# copy the images subdirectory from OFEP to docs/source
if not os.path.exists(destination_subdirectory):
    os.makedirs(destination_subdirectory)


for filename in os.listdir(source_subdirectory):
    source_file = os.path.join(source_subdirectory, filename)
    destination_file = os.path.join(destination_subdirectory, filename)

    # Check if the file is a PNG file (case-insensitive)
    if filename.lower().endswith('.png'):
        shutil.copy2(source_file, destination_file)  # Copy the file
