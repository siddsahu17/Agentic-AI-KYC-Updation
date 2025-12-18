import asyncio
import random

async def run_kyc_agent(document_paths: list[str]):
    """
    Placeholder for AI agent.
    Returns mocked extracted KYC JSON.
    """
    # Simulate processing delay
    await asyncio.sleep(2)

    # Mocked data
    mock_data = {
        "full_name": "Siddhant Sahu",
        "dob": "1995-08-15",
        "gender": "Male",
        "address": "123, AI Lane, Tech City, Bangalore, India",
        "id_number": "1234-5678-9012",
        "id_type": "Aadhaar"
    }
    
    return mock_data
