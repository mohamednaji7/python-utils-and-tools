import time
import logging
import json
import os

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install
install()
console = Console()


def init_logger(rich_print_or_logs='logs'):
    global logger
    logger = Logger(rich_print_or_logs).logger


class Logger:
    def __init__(self, rich_print_or_logs='rich_print'):
        self.rich_print_or_log = rich_print_or_logs
        if self.rich_print_or_log == 'rich_print':
            self.logger = console.print
        else:
            logging.basicConfig(
                level=logging.INFO,
                format="%(message)s",
                datefmt="[%X]",
                handlers=[RichHandler(console=console)]
            )
            self.logger = logging.getLogger("rich")


class TimeEstimator:
    def __init__(self, number_of_iterations):
        self.processing_time = 0.0
        self.iter_index = 0
        self.total_number_of_iterations = number_of_iterations
    
    def start_iteration(self):
        self.start_time = time.time()
        if self.iter_index == 0:
            logger.info(f"Started iteration: {self.iter_index}/{self.total_number_of_iterations}")
        else:
            logger.info(f"Remaining time: {self.processing_time * self.total_number_of_iterations / 60:.2f} minutes, iter: {self.iter_index}/{self.total_number_of_iterations}")

    def update_processing_time(self):
        processing_time = time.time() - self.start_time
        self.processing_time = (self.processing_time + processing_time) / (2 if self.iter_index > 0 else 1)
        self.iter_index += 1

class FileSystemProcessor:
    def __init__(self, root_dir, process_subdirs=False):
        self.root_dir = root_dir
        self.process_subdirs = process_subdirs
    
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
