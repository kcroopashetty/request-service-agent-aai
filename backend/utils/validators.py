"""Input validation utilities"""
import re
from typing import Optional

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_employee_id(emp_id: str) -> bool:
    return bool(re.match(r'^EMP\d{3}$', emp_id))

def validate_request_id(req_id: str) -> bool:
    return bool(re.match(r'^REQ\d{3}$', req_id))

def validate_status(status: str) -> bool:
    valid_statuses = ['pending', 'approved', 'rejected', 'cancelled']
    return status.lower() in valid_statuses

def validate_request_type(req_type: str) -> bool:
    valid_types = ['laptop', 'mobile', 'travel', 'expense', 'desk_phone']
    return req_type.lower() in valid_types

def sanitize_input(text: str, max_length: int = 255) -> str:
    return text.strip()[:max_length]
