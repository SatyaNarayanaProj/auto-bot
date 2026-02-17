from playwright.sync_api import sync_playwright
import os
import re



URL = "https://hrms-420.netlify.app"

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

EMAIL_SELECTOR = 'input[type="email"]'
PASS_SELECTOR = 'input[type="password"]'
LOGIN_BTN = 'button[type="submit"]'


def run():

    if not EMAIL or not PASSWORD:
        raise ValueError("EMAIL or PASSWORD secret missing")

    with sync_playwright() as p:

        print("Launching browser...")

        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        page = browser.new_page()


        print("Opening site...")
        page.goto(URL, wait_until="domcontentloaded")


        print("Waiting for login form...")
        page.wait_for_selector(EMAIL_SELECTOR, timeout=60000)

        print("Entering credentials...")
        page.fill(EMAIL_SELECTOR, EMAIL)
        page.fill(PASS_SELECTOR, PASSWORD)

        print("Submitting login...")
        page.click(LOGIN_BTN)

        print("Waiting for Punch button...")

        punch_btn = page.get_by_role(
            "button",
            name=re.compile(r"Punch (In|Out)", re.IGNORECASE)
        )

        punch_btn.wait_for(state="visible", timeout=60000)

        label = punch_btn.inner_text()
        print("Detected button:", label)


        print("Clicking attendance button...")
        punch_btn.click()

        page.wait_for_timeout(3000)

        print("Attendance marked successfully ✓")

        browser.close()


if __name__ == "__main__":
    run()
