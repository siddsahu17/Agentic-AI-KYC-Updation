import re
from datetime import datetime
from .validator import calculate_confidence

def extract_aadhaar_fields(ocr_text: str) -> dict:
    """
    Extracts Aadhaar fields using regex and heuristics.
    """
    data = {
        "fullName": "",
        "dob": "",
        "gender": "",
        "address": "",
        "idNumber": "",
        "idType": "Aadhaar",
        "confidence": "low"
    }
    
    # 1. Extract Aadhaar Number (12 digits, often spaced 4-4-4)
    # Regex looks for 4 digits space 4 digits space 4 digits, or just 12 digits
    aadhaar_pattern = r'\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b'
    aadhaar_match = re.search(aadhaar_pattern, ocr_text)
    if aadhaar_match:
        data["idNumber"] = aadhaar_match.group(0).replace(" ", "")

    # 2. Extract DOB (DD/MM/YYYY or YYYY-MM-DD)
    dob_pattern = r'\b(\d{2}/\d{2}/\d{4})\b|\b(\d{4}-\d{2}-\d{2})\b'
    dob_match = re.search(dob_pattern, ocr_text)
    if dob_match:
        raw_dob = dob_match.group(0)
        # Normalize to YYYY-MM-DD
        try:
            if "/" in raw_dob:
                dt = datetime.strptime(raw_dob, "%d/%m/%Y")
                data["dob"] = dt.strftime("%Y-%m-%d")
            else:
                data["dob"] = raw_dob
        except ValueError:
            pass # Keep empty if parsing fails

    # 3. Extract Gender
    if "MALE" in ocr_text.upper():
        data["gender"] = "Male"
    elif "FEMALE" in ocr_text.upper():
        data["gender"] = "Female"
    elif "TRANSGENDER" in ocr_text.upper():
        data["gender"] = "Transgender"

    # 4. Extract Name (Heuristic: Line before DOB or near top)
    # This is tricky with raw OCR. We'll try to find a line that looks like a name.
    # Often in Aadhaar, name is English and local language. 
    # We'll use a placeholder LLM function for better extraction later.
    data["fullName"] = llm_extract_name(ocr_text)
    
    # 5. Extract Address
    # Address usually starts with "Address:" or "To:" on the back side.
    # For now, we'll try to capture a block of text.
    data["address"] = llm_extract_address(ocr_text)
    
    # Calculate confidence
    data["confidence"] = calculate_confidence(data)
    
    return data

def llm_extract_name(text: str) -> str:
    """
    Placeholder for LLM-based name extraction.
    Simple heuristic: Look for lines that are not keywords.
    """
    lines = text.split('\n')
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue
        # Skip keywords
        if any(k in clean_line.upper() for k in ["GOVERNMENT", "INDIA", "UIDAI", "AADHAAR", "DOB", "YEAR", "MALE", "FEMALE"]):
            continue
        # Skip numbers
        if re.search(r'\d', clean_line):
            continue
        # Assume first valid line is name (very naive)
        return clean_line
    return ""

def llm_extract_address(text: str) -> str:
    """
    Placeholder for LLM-based address extraction.
    """
    # Look for "Address" keyword
    match = re.search(r'Address:?\s*(.*)', text, re.IGNORECASE | re.DOTALL)
    if match:
        # Take up to 100 chars or newline
        return match.group(1).strip()[:100].replace('\n', ', ')
    return ""
