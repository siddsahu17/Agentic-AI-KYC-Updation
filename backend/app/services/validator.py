import re
from datetime import datetime

def validate_aadhaar_number(number: str) -> bool:
    """
    Validates Aadhaar number format (12 digits).
    Does not perform Verhoeff algorithm check for simplicity, but checks length and digits.
    """
    if not number:
        return False
    # Remove spaces and hyphens
    clean_number = re.sub(r'[\s-]', '', number)
    return bool(re.match(r'^\d{12}$', clean_number))

def validate_dob(dob: str) -> bool:
    """
    Validates DOB format (YYYY-MM-DD).
    """
    if not dob:
        return False
    try:
        datetime.strptime(dob, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_name(name: str) -> bool:
    """
    Validates name is non-empty and has reasonable length.
    """
    if not name:
        return False
    return len(name.strip()) > 2

def validate_address(address: str) -> bool:
    """
    Validates address is non-empty and has min length.
    """
    if not address:
        return False
    return len(address.strip()) > 10

def calculate_confidence(data: dict) -> str:
    """
    Calculates overall confidence based on field validation.
    """
    score = 0
    total_checks = 4
    
    if validate_aadhaar_number(data.get("idNumber")):
        score += 1
    if validate_dob(data.get("dob")):
        score += 1
    if validate_name(data.get("fullName")):
        score += 1
    if validate_address(data.get("address")):
        score += 1
        
    if score == 4:
        return "high"
    elif score >= 2:
        return "medium"
    else:
        return "low"
