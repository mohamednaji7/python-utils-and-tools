
import magic
import json

import os
import shutil
import subprocess
import sys

from rich.console import Console
from rich.progress import Progress

import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def get_file_duration(file_path):
    """Get the duration of the audio or video file using ffprobe."""
    cmd = [
        "ffprobe", "-i", file_path,
        "-show_entries", "format=duration",
        "-v", "quiet",
        "-of", "csv=p=0"
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    duration = float(result.stdout.strip())
    return duration



def has_audio_stream(file_path):
    """Check if the audio or video file has an audio stream."""
    cmd = [
        "ffprobe", "-i", file_path,
        "-show_streams", "-select_streams", "a",
        "-loglevel", "error"
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return bool(result.stdout.strip())

def get_durations(files):
    durations = []

    for i, file in enumerate(files):
        file_path = file['FILE_PATH']

        # Print progress in the format i/len(files)
        print(f"🔄  📂  Processing {i+1}/{len(files)}", end="\r")

        # Check if file exists
        if not os.path.exists(file_path):
            durations.append(0)
            print(f"📄  ❌  {i+1}/{len(files)} File does not exist: {file_path}")
            continue

        # Check if file has an audio stream
        if not has_audio_stream(file_path):
            durations.append(0)
            print(f"🔇  ❌  {i+1}/{len(files)} No audio stream found: {file_path}")
            continue
        try:
            durations.append(int(get_file_duration(file_path)))

        except Exception as e:
            print(f"🛠️  ❌  {i+1}/{len(files)} Could not process {file_path}: {e}")
            durations.append(0)

    print("\n✅  Returned all file durations.")
    return durations


def get_names(files):
    """
    Generates descriptive names for files based on their directory and index.
    Shows directory names with indices when a new directory starts or at key points.

    Args:
        files (list of dict): Each dict should have a 'FILE_PATH' key.

    Returns:
        list: List of names, with "" for subsequent files in the same directory.
    """
    names = []
    prev_dir = None  # Track the previous directory

    for i, file in enumerate(files):
        print(f"🔄  📂  Processing {i+1}/{len(files)}", end="\r")
        file_path = file['FILE_PATH']
        file_dir = os.path.basename(os.path.dirname(file_path))  # Get the last directory in the path

        if file_dir != prev_dir:
            # Show directory name with index when it's the first file in a new directory
            names.append(file_dir)
            prev_dir = file_dir
        else:
            # Use empty string for subsequent files in the same directory
            names.append("")

    print("\n✅  Done making all names.")
    return names


def check_files_states(files, statuses):
    """
    Returns:
        statuses (list): List of statuses for each file ('error', 'done', 'pending').
    """
    for i, file in enumerate(files):
        TRANSLATE = file['TRANSLATE']
        file_path = file['FILE_PATH']
        if not os.path.exists(file_path) or not has_audio_stream(file_path):
            statuses[i] = "error"
            print(i+1, statuses[i]," "*5,   end =" ")
            continue

        output_path = file_path.replace(".MP4", "")
        output_path = output_path.replace(".mp4", "")

        output_path = output_path + f'-transcription{"-translated" if TRANSLATE else ""}.txt' 

        print(output_path)
        if os.path.exists(output_path):
            statuses[i] = "done"

    print("✅  Done checking all files.")
    return statuses

def save_plot_file_durations(names, durations, statuses, verbose=False):
    """
    Plots file durations with color coding based on processing status.

    Args:
        names (list): List of file names or identifiers.
        durations (list): List of durations corresponding to each file.
        statuses (list): List of statuses for each file ('error', 'done', 'pending').

    Status Mapping:
        - 'error' → Red bar
        - 'done' → Green bar
        - 'pending' → Blue bar
    """
    # Map statuses to colors
    status_colors = {
        'error': 'red',
        'done': 'green',
        'pending': 'blue'
    }

    # Generate indices for the files
    file_indices = list(range(1, len(names) + 1))

    # Plot
    plt.figure(figsize=(14, 8))
    bars = plt.barh(file_indices, durations, color=[status_colors[status] for status in statuses])

    plt.xlabel('Duration (seconds)')
    plt.ylabel('Files')
    plt.title('Processing Audio/Video.')

    # Add file names or identifiers to the y-axis
    # plt.yticks(file_indices, names)
    plt.yticks(file_indices, names, fontsize=8)  # Adjust fontsize as needed


    # Add a legend
    legend_patches = [
        Patch(color='blue', label='Pending'),
        Patch(color='red', label='Error'),
        Patch(color='green', label='Done'),
    ]
    plt.legend(handles=legend_patches, loc='upper right')

    plt.tight_layout()
    plot_filename = 'file_durations_plot.png'

    plt.savefig(plot_filename)

    if not sys.stdout.isatty():
        plt.show()
    plt.close()

    if verbose:
        print(f"✅  💾  Plot saved as {plot_filename}")
        error_count = statuses.count('error')
        print(f"Total Errors: {error_count}")




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





# # Initialize the JSON structure
# json_data = {
#     "MODEL": "large-v3",
#     "GPU": True,
#     "FILES": []
# }



# input_dir = base_dir + videos_dir



def dir_tree_to_json(input_dir, json_data):

    output_json = input_dir + ' - videos.json'

    add_dir_files_to_json(input_dir, file_language="en", translate=False, timestamp=True, json_data=json_data)

    # Write the JSON data to the output file
    with open(output_json, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)

    print(f"JSON file has been created: {output_json}")
    
    return output_json 
