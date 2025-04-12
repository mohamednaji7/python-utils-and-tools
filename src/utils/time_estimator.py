import time
from .logger import logger  # Import logger

class TimeEstimator:
    def __init__(self, number_of_iterations):
        # Ensure number_of_iterations is at least 1 to avoid division by zero later
        if number_of_iterations <= 0:
            raise ValueError("Number of iterations must be positive.")
            
        self.average_iteration_time = 0.0  # Renamed for clarity
        self.iter_index = 0
        self.total_number_of_iterations = number_of_iterations
        self.start_time = None # Initialize start_time

    def start_iteration(self):
        """Call this at the beginning of each iteration."""
        self.start_time = time.time() # Record start time for the current iteration
        
        remaining_iterations = self.total_number_of_iterations - self.iter_index
        
        if self.iter_index == 0:
            logger.info(f"Starting process: {self.iter_index + 1}/{self.total_number_of_iterations} iterations")
        else:
            # Calculate remaining time only if we have an average time estimate
            if self.average_iteration_time > 0:
                # Correct calculation: average_time * remaining_iterations
                estimated_remaining_seconds = self.average_iteration_time * remaining_iterations
                estimated_remaining_minutes = estimated_remaining_seconds / 60
                logger.info(f"Est. remaining time: {estimated_remaining_minutes:.2f} minutes. "
                            f"Starting iteration: {self.iter_index + 1}/{self.total_number_of_iterations}")
            else:
                 # Cannot estimate yet
                 logger.info(f"Starting iteration: {self.iter_index + 1}/{self.total_number_of_iterations}")

    def update_processing_time(self):
        """Call this at the end of each iteration to update estimates."""
        if self.start_time is None:
            logger.warning("end_iteration called before start_iteration for the current cycle.")
            return # Or raise an error

        current_iteration_duration = time.time() - self.start_time
        
        # Correct Running Average Calculation:
        # new_avg = (old_avg * old_count + new_value) / (old_count + 1)
        # In our case: old_count is self.iter_index (0 for the first iter, 1 for second, etc.)
        #              new_value is current_iteration_duration
        #              new_count is self.iter_index + 1
        self.average_iteration_time = (self.average_iteration_time * self.iter_index + current_iteration_duration) / (self.iter_index + 1)
        
        self.iter_index += 1 # Increment index AFTER calculations for the completed iteration
        self.start_time = None # Reset start time until next start_iteration call

    def get_estimated_total_time(self):
        """Returns the estimated total time in seconds based on the current average."""
        if self.average_iteration_time > 0:
            return self.average_iteration_time * self.total_number_of_iterations
        else:
            return 0.0 # Cannot estimate yet

    def get_estimated_remaining_time(self):
         """Returns the estimated remaining time in seconds based on the current average."""
         if self.average_iteration_time > 0 and self.iter_index < self.total_number_of_iterations:
             remaining_iterations = self.total_number_of_iterations - self.iter_index
             return self.average_iteration_time * remaining_iterations
         else:
             return 0.0 # Cannot estimate or process finished
         
         
# class TimeEstimator:
#     def __init__(self, number_of_iterations):
#         self.total_time = 0.0
#         self.iter_index = 0
#         self.total_number_of_iterations = number_of_iterations

#     def start_iteration(self):
#         self.start_time = time.time()

#         if self.iter_index == 0:
#             logger.info(f"Started iteration: {self.iter_index}/{self.total_number_of_iterations}")
#         else:
#             avg_time = self.total_time / self.iter_index
#             remaining_iters = self.total_number_of_iterations - self.iter_index
#             remaining_minutes = (avg_time * remaining_iters) / 60
#             logger.info(f"Remaining time: {remaining_minutes:.2f} minutes, iter: {self.iter_index}/{self.total_number_of_iterations}")

#     def update_processing_time(self):
#         processing_time = time.time() - self.start_time
#         self.total_time += processing_time
#         self.iter_index += 1
