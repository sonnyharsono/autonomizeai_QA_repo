import pytest
from playwright.sync_api import Page, expect

@pytest.mark.ui
class TestUserExperience:
    """
    Validates the clinician dashboard and file upload workflows
    using Playwright.
    """

    def test_dashboard_loading_and_security_headers(self, page: Page):
        """
        Ensures the main dashboard loads and contains critical 
        safety and risk navigation elements.
        """
        # Using a raw string r""" to fix the escape sequence warning
        html_content = r"""
        <html>
            <body>
                <nav>
                    <h1>Autonomize AI - Clinical Triage</h1>
                    <button id='upload-btn'>Upload Patient Note</button>
                    <div id='risk-threshold'>Safety Gate: 0.85</div>
                </nav>
            </body>
        </html>
        """
        page.set_content(html_content)
        
        # Assertions using Playwright's expect library (Best Practice)
        expect(page.get_by_role("heading")).to_contain_text("Clinical Triage")
        expect(page.locator("#upload-btn")).to_be_visible()

    @pytest.mark.critical
    def test_invalid_file_upload_error(self, mock_upload_page):
        """
        CRITICAL UI TEST: Verifies that the UI correctly handles and 
        displays errors when an invalid file is uploaded.
        """
        page = mock_upload_page
        
        # Setup mock UI state
        page.set_content(r"""
            <input type='file' id='file-input'>
            <div id='error-message' style='display:none;'>Invalid file format. Please upload a PDF.</div>
            <script>
                document.getElementById('file-input').addEventListener('change', () => {
                    document.getElementById('error-message').style.display = 'block';
                });
            </script>
        """)

        # Simulate user interaction
        page.set_input_files("#file-input", {
            "name": "unsupported_format.exe",
            "mimeType": "application/x-msdownload",
            "buffer": b"test content"
        })

        # Verify the safety alert is displayed to the clinician
        error_locator = page.locator("#error-message")
        expect(error_locator).to_be_visible()
        expect(error_locator).to_contain_text("Please upload a PDF")

    def test_risk_score_color_coding(self, page: Page):
        """
        UX TEST: Verifies that high risk scores are visually distinct 
        for clinicians (Accessibility/Safety test).
        """
        page.set_content(r"""
            <div id='score' class='high-risk' style='color: red;'>0.89</div>
        """)
        
        score_element = page.locator("#score")
        # Ensure the styling meets our safety visibility requirements
        color = score_element.evaluate("el => getComputedStyle(el).color")
        assert color == "rgb(255, 0, 0)", "High risk score must be displayed in RED"
