import logging
import os
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_folder = "LOG"
        os.makedirs(self.log_folder, exist_ok=True)

        # Generate log filename with timestamp
        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        self.log_file = os.path.join(self.log_folder, f"{timestamp}.txt")

        # Configure logging
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            encoding="utf-8",
        )

    def log_print(self, msg):  # Added 'self'
        logging.info(msg)
        print(msg)

