import os
import logging
from datetime import datetime

def setup_logging():
    """ Set up logging with a new file for each day. """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logging.basicConfig(filename=os.path.join(log_dir, datetime.now().strftime('%Y%m%d.log')),
                        level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

def load_base_context():
    with open("config/prompt.txt", "r", encoding="utf-8") as file:
        return file.read().strip()
