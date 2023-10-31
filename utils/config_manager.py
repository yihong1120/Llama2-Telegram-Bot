import os
import logging
from datetime import datetime

def setup_logging() -> None:
    """
    Set up logging with a new file for each day. 

    This function checks if a directory named "logs" exists, if not, it creates one. 
    It sets up basic logging configuration with a new log file for each day. 
    The log files are named according to the current date (YYYYMMDD.log format).
    It also adds a stream handler to the root logger, which logs INFO and higher level messages to the console.
    """
    # Directory where the log files will be stored
    log_dir = "logs"
    
    # Check if the directory exists, if not, create it
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # Set up basic logging configuration
    logging.basicConfig(filename=os.path.join(log_dir, datetime.now().strftime('%Y%m%d.log')),
                        level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a stream handler that logs to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    
    # Add the console handler to the root logger
    logging.getLogger().addHandler(console)

def load_base_context() -> str:
    """
    Load the base context from a file.

    This function reads the base context from a file named "prompt.txt" located in the "config" directory.

    Returns:
        str: The content of the file.
    """
    # Open the file in read mode and return its content
    with open("config/prompt.txt", "r", encoding="utf-8") as file:
        return file.read().strip()
