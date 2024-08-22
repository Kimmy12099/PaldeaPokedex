import os

def rename_files(folder_path):
    # Get the list of files in the folder
    files = os.listdir(folder_path)

    for file_name in files:
        # Check if the file is a PNG file
        if file_name.lower().endswith('.png'):
            # Extract the base name and extension
            base_name, ext = os.path.splitext(file_name)

            # Process only if base_name is a number
            if base_name.isdigit():
                number = int(base_name)

                if number < 100:
                    # Add leading zeros to numbers from 0 to 99
                    new_base_name = f'{number:03}'  # Format with leading zeros (e.g., 001, 023)
                else:
                    # Remove leading zeros from four-digit numbers
                    new_base_name = str(number)

                new_name = f'{new_base_name}{ext}'

                # Construct full paths for renaming
                old_path = os.path.join(folder_path, file_name)
                new_path = os.path.join(folder_path, new_name)

                # Rename the file
                os.rename(old_path, new_path)
                print(f'Renamed: {file_name} -> {new_name}')
            else:
                print(f'Skipping non-numeric file: {file_name}')

# Example usage
folder_path = 'Pokemon_Images'  # Replace with the path to your folder
rename_files(folder_path)
