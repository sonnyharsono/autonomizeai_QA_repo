# Autonomize AI: Clinical Safety & Agentic Platform Validation Framework

**Candidate:** Sonny Harsono  
**Role:** Senior QA Engineer Candidate

## 1. Executive Summary: Test Methodology & Strategy

This submission presents a comprehensive, **CI/CD-ready test framework** designed to validate the core components of the Agentic Healthcare Platform. Our strategy is built on **Risk-Based Testing**, prioritizing **Clinical Safety** and **Data Integrity** above all else.

We employ a **Hybrid Validation Approach** to test the system's different layers:
1.  **Probabilistic Validation:** Testing the AI Model's outputs against defined clinical safety thresholds and semantic coherence.
2.  **Deterministic Validation:** Testing the Data Extraction Agents and UI for strict adherence to schemas and business logic.

---

## 2. High-Level Design (HLD) & Model Context

### System Context
The Agentic Platform's primary goal is to **triage patient records** for clinical urgency. This relies on the seamless handover of data from the **Extraction Agent** to the **Risk Model**.

### Clinical Risk Classification Model
| Component | Description | Safety Threshold |
| :--- | :--- | :--- |
| **Model Purpose** | Triage unstructured patient notes for severity. Output is used to place the patient record into a clinician review queue. | **HIGH RISK ($\ge 0.85$):** Triggers an immediate P1 alert, overriding conflicting low-severity keywords. |
| **Testing Focus** | **Semantic Coherence:** Does the model understand the nuance between "mild cough" and "patient collapsed?" |
| **Failure Mode** | Model bias or insufficient weighting of critical clinical keywords (e.g., *syncope*, *thoracic pain*). |



### Data Extraction Agent (OCR)
| Component | Description | Compliance Focus |
| :--- | :--- | :--- |
| **Agent Purpose** | Convert unstructured data (faxes, PDFs) into structured JSON format. | **FHIR/ICD-10 Compliance:** Ensuring extracted diagnosis codes are in the correct format (e.g., must start with a letter). |
| **Testing Focus** | **Data Integrity:** Accuracy of field extraction, handling of noisy input (low confidence). |

---

## 3. Detailed Test Cases (Manual / Documentation)

The following table outlines the **Manual Test Cases** (formatted for tracking in tools like Jira or Zephyr) that correspond to the automated scripts in the `tests/` directory.

| Test ID | Scenario & Priority | Steps to Reproduce | Expected Result (Pass Criteria) |
| :--- | :--- | :--- | :--- |
| **M-001** | **Model Safety Critical (P1)** | 1. Provide input: "Patient reports mild discomfort, but spouse mentions patient **clutched chest and collapsed**." 2. Review Model API output. | `risk_score` must be $\ge 0.85$. **Failure if** `risk_score` is low, indicating a potential safety override failure. |
| **A-001** | **Agent Data Integrity (P2)** | 1. Provide mock "Noisy Fax" input (where OCR reads 'I10' as '110'). 2. Review Agent output JSON. | `diagnosis_code` must be flagged as non-compliant (numeric instead of alphanumeric), OR `confidence_score` must be $\le 0.80$ to trigger human review. |
| **UI-001** | **UX/UI Validation (P3)** | 1. Attempt to upload a non-medical, non-PDF file (`.exe` or `.zip`). 2. Observe the interface. | User interface prevents the upload, and a clear, non-technical error message ("Invalid File Format") is displayed to the end-user. |

---

## 4. Automation Framework & Execution

### Tech Stack
* **Language:** Python 3.9+
* **Framework:** Pytest (for structured test execution and fixtures)
* **UI Automation:** Playwright (for reliable end-to-end testing)
* **Reporting:** Pytest-HTML

### Repository Structure (Aligned Framework)
The framework is aligned using a dedicated `tests/` directory and `conftest.py` for centralized setup (fixtures/mocks).

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers for UI test
playwright install
