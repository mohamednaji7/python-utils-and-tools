
import magic
import json

import os
import shutil
from rich.console import Console
from rich.progress import Progress



def test_writing_empty_files(base_directory, directory):
    """
    Test creating directories and saving empty .txt files in the specified directory structure.
    """
    
    
    input_dir = os.path.join(base_directory, directory)
    test_directory = os.path.join(base_directory, directory + " Testing writing all the files")
    console = Console()
    
    console.print(os.listdir(os.path.join(base_directory, directory)))

    error_files = []  # To track files with errors
    total_files = 0  # To count total .mp4 files processed
    total_non_mp4_files = 0  # To count total non-.mp4 files
    non_mp4_files = []  # To track non-.mp4 files
    success_files = 0  # To count successfully written files
    existing_files = 0  # To count the files that actually exist (not just processed)

    # Walk through the input directory and process each file
    with Progress() as progress:
        task = progress.add_task("Processing files...", total=0)

        for root, dirs, files in os.walk(input_dir):
            for filename in files:
                existing_files += 1  # Count all files that exist
                input_path = os.path.join(root, filename)
                if not os.path.isfile(input_path):
                    continue
                # print file path
                # console.print(input_path)
                # if filename.lower().endswith('.mp4'):
                # if 'video' in magic.from_file(input_path, mime=True):
                if filename.lower().endswith('.mp4') or 'video' in magic.from_file(input_path, mime=True):

                    total_files += 1  # Count total .mp4 files
                    progress.update(task, description=f"Processing {filename}...", advance=1)

                    try:
                        # Determine the relative path from the base input directory
                        relative_path = os.path.relpath(root, input_dir)
                        output_dir = os.path.join(test_directory, relative_path)

                        # Create the output directory if it doesn't exist
                        os.makedirs(output_dir, exist_ok=True)

                        # Create an empty .txt file in the corresponding output directory
                        output_path = os.path.join(output_dir, filename)
                        with open(output_path, 'w', encoding='utf-8') as file:
                            file.write('')  # Write an empty file
                        success_files += 1

                    except Exception as e:
                        error_files.append((filename, str(e)))
                else:
                    total_non_mp4_files += 1  # Count non-.mp4 files
                    non_mp4_files.append(filename)

    # Print the summary
    console.print("\n📊 Summary:", style="bold blue")
    console.print(f"📁 Total files found: {existing_files}")
    console.print(f"🎥 Total .mp4 files: {total_files}")
    console.print(f"📂 Total non-.mp4 files: {total_non_mp4_files}")
    console.print(f"📂 Total files processed: {total_files}")  # Files that were processed (all .mp4)
    console.print(f"✔️ Successfully written files: {success_files}")
    console.print(f"❌ Files with errors: {len(error_files)}")

    if len(error_files) > 0:
        console.print(f"📝 Details of errors above.", style="bold red")
    else:
        console.print("✅ No errors occurred.", style="bold green")

    # Ask the user if they want to print the errors
    if error_files:
        user_input = input("\n❓ Do you want to print the errors? (yes/no): ").strip().lower()
        if user_input == 'yes':
            console.print("\n❌ Files with errors during writing:", style="bold red")
            for filename, error in error_files:
                console.print(f"\n{filename} - ERROR:\n{error}", style="bold red")
    else:
        console.print("✅ All directories and files were created successfully.", style="bold green")

    # Clean up the test directory after the process
    if os.path.exists(test_directory):
        shutil.rmtree(test_directory)
        console.print(f"\n🧹 The test directory '{test_directory}' has been deleted.", style="bold yellow")


    # print(f"Skipping non-.mp4 file: {filename}")
    console.print(non_mp4_files)

# Usage

# # Test writing empty files
# test_writing_empty_files(base_dir, videos_dir)

def clean_timestamp_from_lines(input_dir, verbose=1):
    """
    Recursively processes all files in input_dir and its subdirectories.
    For each file, cleans out timestamp patterns like '[102:15 - 102:20]' from the lines without removing the whole line.
    Modifies files in-place.
    
    Args:
        input_dir (str): Path to the input directory containing transcription files
    """
    # Regular expression to match timestamp patterns like [102:15 - 102:20], [1:15 - 10:20]
    timestamp_pattern = re.compile(r'\[\d+:\d+ - \d+:\d+\]')
    
    # Counters
    files_cleaned = 0
    files_processed = 0
    total_files = 0
    timestamps_cleaned = 0
    
    # Walk through all files and directories in the input directory
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            total_files += 1
            
            try:
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                # Clean out timestamps from each line
                cleaned_lines = []
                file_timestamps_cleaned = 0
                
                for line in lines:
                    # Replace timestamp pattern with an empty string
                    cleaned_line = timestamp_pattern.sub('', line)
                    if cleaned_line != line:  # If a change was made
                        file_timestamps_cleaned += 1
                    cleaned_lines.append(cleaned_line.strip())
                
                # If any timestamps were cleaned, update counters and write back the file
                if file_timestamps_cleaned > 0:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        # file.writelines("\n".join(cleaned_lines)+"\n")
                        file.writelines("\n".join(cleaned_lines))
                    
                    files_cleaned += 1
                    timestamps_cleaned += file_timestamps_cleaned
                    if verbose > 1: print(f"Processed {file_path}: Cleaned {file_timestamps_cleaned} timestamp occurrences")

                files_processed += 1
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
    
    if verbose: print(f"Completed cleaning {files_cleaned} files. Total timestamps cleaned: {timestamps_cleaned}")
    if verbose: print(f"Total files: {total_files}, Files processed: {files_processed}")




def add_dir_files_to_json(input_dir, file_language, translate, timestamp, json_data):
    # Walk through the MERE directory and subdirectories
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            # if file.endswith('.MP4') or file.endswith('.mp4'):
            # if  file.endswith('.mp4'):

            file_path = os.path.join(root, file)

            if file.lower().endswith('.mp4') or 'video' in magic.from_file(file_path, mime=True):

                # print(file_path)

                file_entry = {
                    "FILE_PATH": file_path,
                    "FILE_LANGUAGE": file_language,  # You can adjust this based on your requirement
                    "TRANSLATE": translate,
                    "TIMESTAMP": timestamp
                }
                json_data["FILES"].append(file_entry)





def dir_tree_to_json(input_dir, json_data, timestamp=True):

    output_json = input_dir + ' - videos.json'

    add_dir_files_to_json(input_dir, file_language="en", translate=False, timestamp=timestamp, json_data=json_data)

    # Write the JSON data to the output file
    with open(output_json, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)

    print(f"JSON file has been created: {output_json}")
    
    return output_json 
