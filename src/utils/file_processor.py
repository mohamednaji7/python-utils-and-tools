
from utils.logger import logger  # Import logger
import os
import json


class FileSystemProcessor:
    def __init__(self, root_dir, process_subdirs=False):
        self.root_dir = root_dir
        self.process_subdirs = process_subdirs
    
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
