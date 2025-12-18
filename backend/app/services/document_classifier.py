def classify_document(text: str) -> str:
    """
    Classifies the document based on OCR text content.
    Returns "AADHAAR" or "UNKNOWN".
    """
    text_upper = text.upper()
    
    aadhaar_keywords = [
        "GOVERNMENT OF INDIA",
        "UIDAI",
        "UNIQUE IDENTIFICATION AUTHORITY OF INDIA",
        "AADHAAR",
        "MERA AADHAAR",
        "MERI PEHCHAN"
    ]
    
    for keyword in aadhaar_keywords:
        if keyword in text_upper:
            return "AADHAAR"
            
    return "UNKNOWN"
