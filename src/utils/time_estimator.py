import time
from .logger import logger  # Import logger

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