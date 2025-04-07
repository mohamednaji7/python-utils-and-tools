import os
import subprocess
import sys



import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def make_output_path(file_path: str, TRANSLATE: bool) -> str:
    """
    Create the output path for the transcription or translation file.
    """

    # output_path = file_path.replace(".MP4", "")
    # output_path = output_path.replace(".mp4", "")

    # output_path = output_path + f'- transcription{"- translated" if TRANSLATE else ""}.txt' 

    file_name = os.path.splitext(os.path.basename(file_path))[0]
    file_dir = os.path.dirname(file_path)
    output_path = os.path.join(file_dir, f"{file_name}_transcription{'_translation' if TRANSLATE else ''}.txt")
    
    return output_path



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

        output_path = output_path + f'- transcription{"- translated" if TRANSLATE else ""}.txt' 

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


