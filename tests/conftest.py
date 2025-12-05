import pytest

# =======================================================
# CENTRALIZED FIXTURES & MOCKING LOGIC (Addresses Feedback #3)
# =======================================================

class MockExtractionAgent:
    """
    Centralized Agent simulation, accessible by all tests.
    """
    @staticmethod
    def process_document(file_name):
        if "clean_referral" in file_name:
            return {
                "status": "success",
                "extracted_data": {
                    "patient_id": "P-998877",
                    "first_name": "John",
                    "last_name": "Doe",
                    "dob": "1980-05-12",
                    "diagnosis_code": "I10",
                    "confidence_score": 0.99
                }
            }
        elif "noisy_fax" in file_name:
            return {
                "status": "success",
                "extracted_data": {
                    "patient_id": "P-UNKNOWN",
                    "first_name": "J0hn",
                    "last_name": "Doe",
                    "dob": "1980-05-12",
                    "diagnosis_code": "110",
                    "confidence_score": 0.72
                }
            }
        else:
            return {"status": "failed", "error": "File format not supported"}

# This fixture automatically provides the Agent instance to tests
@pytest.fixture
def extraction_agent():
    return MockExtractionAgent()
