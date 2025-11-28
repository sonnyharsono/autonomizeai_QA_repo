import pytest
import os
from playwright.sync_api import Page, expect

# ==========================================
# MOCK UI SETUP (Simulates the Web Page)
# ==========================================
@pytest.fixture(scope="function")
def mock_upload_page(tmp_path):
    """
    Creates a temporary HTML file to simulate the Patient Upload Portal.
    This ensures the test passes locally without needing a live server.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Upload Medical Record</h1>
        <input type="file" id="file-upload" onchange="validateFile()">
        <div id="error-toast" style="display:none; color:red;">Invalid file format. Only PDF allowed.</div>
        <script>
            function validateFile() {
                const fileInput = document.getElementById('file-upload');
                const filePath = fileInput.value;
                const allowedExtensions = /(\.pdf)$/i;
                if (!allowedExtensions.exec(filePath)) {
                    document.getElementById('error-toast').style.display = 'block';
                    fileInput.value = '';
                    return false;
                }
            }
        </script>
    </body>
    </html>
    """
    # Create the dummy HTML file
    file_path = tmp_path / "upload_mock.html"
    file_path.write_text(html_content)
    return file_path.as_uri()

# ==========================================
# UI TEST SCENARIO
# ==========================================

@pytest.mark.ui
@pytest.mark.critical
def test_invalid_file_upload_error(page: Page, mock_upload_page):
    """
    Scenario: User attempts to upload an .exe file instead of a PDF.
    Expected: Error message 'Invalid file format' appears.
    """
    # 1. Go to the (mock) upload page
    page.goto(mock_upload_page)
    
    # 2. Define an invalid file (simulating a malicious or wrong file)
    # We create a dummy .exe file in memory
    with open("malicious.exe", "w") as f:
        f.write("fake executable code")

    # 3. Upload the invalid file
    # Playwright handles the file chooser dialog
    with page.expect_file_chooser() as fc_info:
        page.locator("#file-upload").click()
        file_chooser = fc_info.value
        file_chooser.set_files("malicious.exe")

    # 4. Assert Error Message Visibility
    error_message = page.locator("#error-toast")
    
    # Wait for error and check text
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Invalid file format")
    
    # Cleanup (remove the fake .exe)
    os.remove("malicious.exe")