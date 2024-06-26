import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setupLogger():
    logger = logging.getLogger('triangle_chess')
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        project_root = os.getenv('PROJECT_ROOT')
        current_datetime = datetime.utcnow()
        formatted_datetime = current_datetime.strftime("%Y_%m_%d-%H")

        log_file_name = f"{formatted_datetime}.log"
        log_file_path = os.path.join(project_root, 'logs', log_file_name)
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        file_handler = RotatingFileHandler(log_file_path, maxBytes=1048576, backupCount=5, encoding="utf-8",mode="a" )
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s \n%(message)s\n')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
