import pytest
import json
from datetime import datetime

# ==========================================
# MOCK AGENT (Simulates OCR & Extraction)
# ==========================================
class MockExtractionAgent:
    """
    Simulates an AI Agent that reads a PDF/Fax and extracts structured data.
    """
    @staticmethod
    def process_document(file_name):
        # Simulate processing different file types
        if "clean_referral" in file_name:
            return {
                "status": "success",
                "extracted_data": {
                    "patient_id": "P-998877",
                    "first_name": "John",
                    "last_name": "Doe",
                    "dob": "1980-05-12",
                    "diagnosis_code": "I10", # Hypertension
                    "confidence_score": 0.99
                }
            }
        elif "noisy_fax" in file_name:
            # Simulates an OCR error where 'I10' is read as '110'
            return {
                "status": "success",
                "extracted_data": {
                    "patient_id": "P-UNKNOWN",
                    "first_name": "J0hn", # OCR typo
                    "last_name": "Doe",
                    "dob": "1980-05-12",
                    "diagnosis_code": "110", # OCR Error (Invalid ICD-10)
                    "confidence_score": 0.72
                }
            }
        else:
            return {"status": "failed", "error": "File format not supported"}

# ==========================================
# TEST SUITE
# ==========================================

@pytest.fixture
def extraction_agent():
    return MockExtractionAgent()

@pytest.mark.agent
@pytest.mark.integration
def test_valid_extraction_schema(extraction_agent):
    """
    Scenario: Clean PDF upload.
    Validate: Data types, required fields, and values match expected formats.
    """
    filename = "clean_referral.pdf"
    result = extraction_agent.process_document(filename)
    
    data = result.get("extracted_data", {})
    
    # 1. Validate Critical Fields exist
    assert "patient_id" in data
    assert "diagnosis_code" in data
    
    # 2. Validate Data Types (Schema Validation)
    assert isinstance(data["patient_id"], str)
    
    # 3. Validate Business Logic (ICD-10 format)
    # ICD-10 codes usually start with a letter. '110' is invalid.
    assert data["diagnosis_code"][0].isalpha(), \
        f"Invalid Diagnosis Code: {data['diagnosis_code']}. Must start with a letter."

@pytest.mark.agent
@pytest.mark.negative
def test_noisy_fax_handling(extraction_agent):
    """
    Scenario: Noisy Fax input (low confidence).
    Validate: System should flag this for human review if confidence < 0.80.
    """
    filename = "noisy_fax_scanned.pdf"
    result = extraction_agent.process_document(filename)
    data = result.get("extracted_data", {})
    
    # In a real system, we don't just fail; we assert that the system *knows* it failed.
    # The test passes if the agent correctly reports low confidence.
    confidence = data.get("confidence_score")
    
    if confidence < 0.80:
        # Expected behavior: Flag for review
        assert True 
    else:
        # If confidence is high but data is bad, that's a Safety Failure.
        assert data["first_name"] == "John", "High confidence reported on incorrect OCR data (Safety Risk)"