# TEST_PLAN.md: Clinical Safety & Agent Validation

## Objective
This document outlines the core test cases for validating the Agentic Platform's data validation and model integration processes, prioritizing **Clinical Safety** and **Data Integrity**. These manual test plans serve as the documentation foundation for the automated tests implemented in the `tests/` directory.

## Test Case Prioritization

| Priority | Risk Profile | Description |
| :--- | :--- | :--- |
| **P1 - Critical** | Direct Patient Safety Risk (e.g., misclassification of a critical symptom). | 
| **P2 - High** | Regulatory/Compliance Risk (e.g., storing non-compliant data) or Core Business Function Failure. |
| **P3 - Medium** | Usability, UX, or Edge Case Failures that are non-critical. |

## Detailed Test Cases

### 1. Model Integration Testing (Clinical Safety Focus)

| Field | Value |
| :--- | :--- |
| **Test ID** | M-001 |
| **Component** | Risk Classification Model API |
| **Priority** | **P1 - Critical** |
| **Automation Ref.** | `test_model_integration.py::test_risk_classification_nuance` |
| **Purpose** | To ensure the model correctly overrides low-severity keywords when a critical safety signal is present (semantic coherence test). |
| **Steps** | 1. Construct patient note payload: "Patient reports mild discomfort, but spouse confirms the patient **clutched chest and collapsed** 30 minutes ago." 2. Send payload to the Model Inference Endpoint. 3. Review the JSON response body. |
| **Expected Result (Pass Criteria)** | **1.** `risk_label` must equal `"HIGH_RISK"`. **2.** `risk_score` must be $\ge 0.85$ (safety threshold). **3.** `confidence_interval` must be $\ge 0.90$. |

### 2. Agent Integration Testing (Data Integrity & Compliance Focus)

| Field | Value |
| :--- | :--- |
| **Test ID** | A-001 |
| **Component** | Data Extraction Agent (OCR/Parsing) |
| **Priority** | **P2 - High** |
| **Automation Ref.** | `test_agent_integration.py::test_noisy_fax_handling` |
| **Purpose** | To validate the Agent's ability to identify low-confidence or non-compliant data (like OCR errors) and flag it for Human-in-the-Loop review. |
| **Steps** | 1. Provide the Agent with simulated **Noisy Fax** data where the ICD-10 code 'I10' is misread as '110' (numeric). 2. Review the output JSON. |
| **Expected Result (Pass Criteria)** | **1.** The extracted `diagnosis_code` field should be invalid per business rules (e.g., must be alphanumeric). **2.** The output `confidence_score` must be $\le 0.80$, proving the agent knows it failed to extract reliable data. |

### 3. UX/UI Validation Testing (User Error Mitigation Focus)

| Field | Value |
| :--- | :--- |
| **Test ID** | U-001 |
| **Component** | Frontend Patient Record Upload Portal |
| **Priority** | **P3 - Medium** |
| **Automation Ref.** | `test_ui_ux.py::test_invalid_file_upload_error` |
| **Purpose** | To prevent users from uploading incorrect file types that could crash the downstream Agent or pose a security risk. |
| **Steps** | 1. Navigate to the Patient Upload Portal URL. 2. Attempt to upload a non-PDF file (e.g., a `.exe` or `.zip` file). |
| **Expected Result (Pass Criteria)** | **1.** The upload process is blocked client-side. **2.** A clear, non-technical error message ("Invalid File Format. Only PDF allowed.") is displayed to the user. |
