# Autonomize AI - Clinical Risk Validation Framework

This repository contains a modular automation framework designed to validate a Healthcare AI pipeline. The system processes unstructured clinical notes, extracts key medical entities, and calculates a triage risk score.

## 🏛 High-Level Design (HLD)
The system is built as a sequential data pipeline with specific safety guardrails at each stage:



1.  **Ingestion Layer:** Receives raw clinical text (e.g., EHR notes).
2.  **Extraction Agent (Natural Language Processing (NLP)):** A deterministic/agentic layer that identifies symptoms, vitals, and history.
    * *Validation:* Focuses on schema accuracy and entity recognition.
3.  **Risk Model (Inference):** A probabilistic engine that assigns a risk score ($R$) and confidence ($C$).
    * *Validation:* Focuses on clinical safety thresholds ($R \ge 0.85$ for critical symptoms).
4.  **UI/UX Dashboard:** Visualizes alerts and triage status for clinicians.

---

## 🛠 Tech Stack & Architecture
- **Language:** Python 3.11 (Pinned for environment stability)
- **Framework:** Pytest (Modular fixtures via `conftest.py`)
- **UI Automation:** Playwright (Page Object Model pattern)
- **CI/CD:** GitHub Actions (Automated Safety Gate)
- **Reporting:** Pytest-HTML with self-contained assets

## 🚀 Getting Started

### Prerequisites
- Python 3.11
- Virtual Environment (recommended)

### Installation
```bash
pip install -r requirements.txt
playwright install --with-deps chromium
