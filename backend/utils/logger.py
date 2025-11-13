"""Enhanced logging utility"""
import logging
from datetime import datetime
import json

class RequestLogger:
    def __init__(self, log_file: str = "requests.log"):
        self.logger = logging.getLogger("RequestService")
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_request(self, action: str, data: dict):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "data": data
        }
        self.logger.info(json.dumps(log_entry))
    
    def log_error(self, error: str, context: dict = None):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "error": error,
            "context": context or {}
        }
        self.logger.error(json.dumps(log_entry))

request_logger = RequestLogger()
