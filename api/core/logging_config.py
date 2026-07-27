import logging
import os


def setup_logging():
    # Create the logs directory if it doesn't already exist.
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler(),  # Also print logs to the terminal.
        ],
    )
