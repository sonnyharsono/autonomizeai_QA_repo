import pytest

@pytest.mark.integration
@pytest.mark.critical
class TestModelIntegration:

    def test_basic_score_calculation(self, risk_model):
        """
        Baseline: Verifies the model returns a valid numerical score.
        """
        data = {"symptoms": ["headache"]}
        score = risk_model.calculate_risk(data)
        
        assert isinstance(score, (int, float))
        assert 0 <= score <= 1.0

    def test_critical_risk_triage_threshold(self, risk_model):
        """
        SAFETY GATE: High-risk symptoms must exceed 0.85 threshold.
        """
        clinical_data = {
            "symptoms": ["chest pain", "shortness of breath"],
            "vitals": {"bp": "160/100"}
        }
        score = risk_model.calculate_risk(clinical_data)
        assert score >= 0.85, f"CRITICAL FAILURE: Safety threshold missed for high-risk symptoms."

    def test_model_uncertainty_handling(self, risk_model):
        """
        Checks if the model correctly flags uncertainty.
        """
        vague_data = {"symptoms": ["unspecified discomfort"]}
        result = risk_model.get_inference_with_confidence(vague_data)
        
        assert "confidence" in result
        if result["confidence"] < 0.70:
            assert result["human_review_required"] is True

    def test_robustness_with_missing_fields(self, risk_model):
        """
        Ensures the model doesn't crash if optional data (vitals) is missing.
        """
        incomplete_data = {"symptoms": ["minor itch"]}
        try:
            score = risk_model.calculate_risk(incomplete_data)
            assert score < 0.30  # Low risk for minor symptom
        except Exception as e:
            pytest.fail(f"Model failed on incomplete input: {e}")
