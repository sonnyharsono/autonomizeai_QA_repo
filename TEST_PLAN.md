---

## 2. TEST_PLAN.md
This document proves you think like a **QA Lead**. It covers what automation *can't* do.

```markdown
# Strategic Test Plan: Clinical Risk Pipeline

## 1. Objective
To ensure 100% reliability of high-risk clinical triage signals and verify that the AI system fails gracefully when presented with ambiguous or malformed medical data.

## 2. Testing Tiers

### Tier 1: Critical (Automated Safety Gate)
* **Trigger:** Every commit/PR.
* **Scope:** High-priority clinical scenarios (e.g., Chest Pain, Stroke symptoms).
* **Pass Criteria:** 100% success on risk scores exceeding $0.85$ for critical inputs.

### Tier 2: Integration (Automated)
* **Scope:** Validating the data contract between the Extraction Agent and the Risk Model.
* **Focus:** Ensuring the Agent doesn't "hallucinate" symptoms not present in the source text.

### Tier 3: Exploratory & Manual (Human-in-the-Loop)
* **Scope:** UX/UI nuances and complex medical edge cases.
* **Focus:** Clinician dashboard usability and alert visibility.



## 3. Clinical Edge Cases (The "Senior" Focus)
| Scenario | Test Method | Expected Behavior |
| :--- | :--- | :--- |
| **Negation Handling** | Integration | "Patient denies chest pain" must NOT trigger a high risk score. |
| **Ambiguous Vitals** | Model Test | Vitals like "BP 120/80?" (with question mark) should trigger low confidence score. |
| **Malformed PDF/OCR** | UI Test | System must show a clear "Extraction Error" toast message. |
| **PHI Leakage** | Security | Verify no Patient Identifiable Information is stored in the Model logs. |

## 4. Risk Mitigation
* **AI Drift:** We implement a baseline "Golden Dataset" to re-validate the model after every update.
* **False Negatives:** The most dangerous risk. We prioritize "Over-Triage" (flagging for human review) over "Under-Triage" (missing a sick patient).
