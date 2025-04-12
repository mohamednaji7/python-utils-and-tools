
from .logger import logger  # Import logger
import os
import json
import shutil

class FileSystemProcessor:
    def __init__(self, root_dir, process_subdirs=False):
        self.root_dir = root_dir
        self.process_subdirs = process_subdirs

    @staticmethod
    def copy_txt_files_preserving_directory_structure(input_dir, verbose=1):
        """
        Copies all .txt files from input_dir and its subdirectories to a new directory
        named '{input_dir} - TXT' while preserving the original directory structure.

        Args:
            input_dir (str): Path to the input directory
        """
        # Create the output directory name
        output_dir = f"{input_dir} - TXT"

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            logger.info(f"Directory '{output_dir}' already exists. Removing it and creating a new one.")
            if input("Do you want to proceed? (y/n): ").lower() != 'y':
                logger.info("Operation cancelled by the user.")
                return
            # If the directory already exists, remove it
            shutil.rmtree(output_dir)
            os.makedirs(output_dir)

        # Walk through all files and directories in the input directory
        for root, dirs, files in os.walk(input_dir):
            # For each file found
            for file in files:
                # Check if it's a .txt file
                if file.endswith('.txt'):
                    # Get the full path of the source file
                    source_file = os.path.join(root, file)

                    # Calculate the relative path from input_dir to get the subdirectory structure
                    rel_path = os.path.relpath(root, input_dir)

                    # Create the destination directory with the same structure
                    if rel_path == '.':
                        # File is in the root input directory
                        dest_dir = output_dir
                    else:
                        # File is in a subdirectory
                        dest_dir = os.path.join(output_dir, rel_path)

                    # Create the destination directory if it doesn't exist
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)

                    # Create the full destination path
                    dest_file = os.path.join(dest_dir, file)

                    # Copy the file
                    shutil.copy2(source_file, dest_file)
                    if verbose>1: print(f"Copied: {source_file} -> {dest_file}")

        if verbose>0: print(f"All .txt files copied to '{output_dir}'")


    @staticmethod
    def backup_file(file_path):
        if os.path.exists(file_path):
            backup_path = f"{file_path}.backup"
            if os.path.exists(backup_path):
                os.remove(backup_path)
            os.rename(file_path, backup_path)
        else:  
            logger.info(f"File not found: {file_path}")
    
    @staticmethod
    # redo the backup function; take in a backup path
    def restore_backup_file(file_path):
        backup_path = f"{file_path}.backup"
        if os.path.exists(backup_path):
            os.rename(backup_path,file_path)
            logger.info(f"Backup file restored: {file_path}")
        else:  
            logger.info(f"File not found: {backup_path}")


    @staticmethod
    def load_json(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    

    

            
    @staticmethod
    def save_json(json_path, json_data, indent=2, append_not_overwrite=True, backup=True, ensure_ascii=False):
        if backup and os.path.exists(json_path):
            backup_path = f"{json_path}.backup"
            if os.path.exists(backup_path):
                os.remove(backup_path)
            os.rename(json_path, backup_path)

        if append_not_overwrite and os.path.exists(json_path):
            logger.error(f"File already exists: {json_path}")
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data.extend(json_data)
                json_data = data

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=indent, ensure_ascii=ensure_ascii)
        logger.info(f"JSON data saved: {json_path}")
