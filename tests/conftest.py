import pytest
from unittest.mock import MagicMock

# --- Global Configurations ---

@pytest.fixture(scope="session")
def safety_thresholds():
    """Returns the core safety metrics defined in the HLD."""
    return {
        "critical_risk": 0.85,
        "confidence_min": 0.70
    }

# --- Extraction Agent Fixtures ---

@pytest.fixture(scope="session")
def mock_extraction_data():
    """Provides a standard 'Golden Data' structure for an extracted patient."""
    return {
        "patient_id": "AUT-99",
        "medical_history": ["hypertension", "diabetes"],
        "symptoms": ["chest pain", "shortness of breath"],
        "symptoms_excluded": ["fever", "nausea"],
        "vitals": {
            "bp": "150/95",
            "heart_rate": 102,
            "oxygen_saturation": 96
        },
        "confidence_score": 0.94,
        "requires_manual_review": False
    }

@pytest.fixture(scope="session")
def extraction_agent(mock_extraction_data):
    """
    Provides a mocked instance of the Extraction Agent.
    In a real scenario, this would interface with the NLP model.
    """
    agent = MagicMock()
    # Default behavior returns the golden data
    agent.process_note.return_value = mock_extraction_data
    return agent

# --- Risk Model Fixtures ---

@pytest.fixture(scope="session")
def risk_model():
    """
    Provides a mocked Risk Model that implements the HLD triage logic.
    """
    model = MagicMock()
    
    def calculate_risk_logic(data):
        # HLD Logic: If critical symptoms exist, return high risk
        critical_keywords = ["chest pain", "shortness of breath", "syncope"]
        symptoms = data.get("symptoms", [])
        
        if any(s in symptoms for s in critical_keywords):
            return 0.89
        return 0.25

    model.calculate_risk.side_effect = calculate_risk_logic
    model.get_inference_with_confidence.return_value = {
        "score": 0.89,
        "confidence": 0.92,
        "human_review_required": False
    }
    return model

# --- UI / Playwright Fixtures ---

@pytest.fixture(scope="function")
def mock_upload_page(page):
    """
    Intercepts network requests to simulate an AI processing state 
    on the frontend without needing a backend server.
    """
    # Example of mocking a backend API response for the UI
    page.route("**/api/v1/upload", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"status": "success", "message": "File processed"}'
    ))
    return page

