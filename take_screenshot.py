"""
Takes a screenshot of the Google Form confirmation page
using Playwright after form submission as proof.
"""
import json
import datetime
from playwright.sync_api import sync_playwright

FORM_CONFIRM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc8RRUAG8n8nPB9dm21m_MxwHQ-JuDnEj7GnvwEkWXykkKFuQ/viewform?usp=sf_link"

def take_screenshot():
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Load submission details
    try:
        with open("submission_details.json") as f:
            details = json.load(f)
        print(f"Submission was for: {details['date']}")
        print(f"Status code: {details['status_code']}")
    except Exception:
        print("No submission details found.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        # Go to the form — it will show "You've already responded" after submission
        print("Opening form page for screenshot...")
        page.goto(FORM_CONFIRM_URL, wait_until="networkidle")
        page.wait_for_timeout(3000)

        screenshot_path = f"form-confirmation-{today}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved: {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    take_screenshot()