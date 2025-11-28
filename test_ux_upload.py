from playwright.sync_api import Page, expect

def test_invalid_file_upload_error(page: Page):
    page.goto("https://platform.autonomize.ai/upload")
    
    # Upload an invalid file type (.exe)
    with page.expect_file_chooser() as fc_info:
        page.click("text=Upload Medical Record")
        file_chooser = fc_info.value
        file_chooser.set_files("tests/data/malicious_script.exe")
        
    # Assert Error Message Clarity
    error_locator = page.locator(".error-toast")
    expect(error_locator).to_be_visible()
    expect(error_locator).to_contain_text("Invalid file type")
    
    # Assert System Stability (Page did not crash/reload)
    expect(page).to_have_url("https://platform.autonomize.ai/upload")