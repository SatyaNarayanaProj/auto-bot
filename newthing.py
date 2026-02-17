from playwright.sync_api import sync_playwright
import os
import re

URL = "https://hrms-420.netlify.app/"

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

EMAIL_SELECTOR = 'input[type="email"]'
PASS_SELECTOR = 'input[type="password"]'
LOGIN_BTN = 'button[type="submit"]'


def run():

    if not EMAIL or not PASSWORD:
        raise ValueError("Missing EMAIL or PASSWORD secrets")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        page = browser.new_page()

        try:
            print("Opening site...")
            page.goto(URL, wait_until="domcontentloaded")

            print("Waiting login form...")
            page.wait_for_selector(EMAIL_SELECTOR, timeout=60000)

            page.fill(EMAIL_SELECTOR, EMAIL)
            page.fill(PASS_SELECTOR, PASSWORD)
            page.click(LOGIN_BTN)

            print("Waiting punch button...")

            punch_btn = page.get_by_role(
                "button",
                name=re.compile(r"Punch (In|Out)", re.IGNORECASE)
            )

            punch_btn.wait_for(timeout=60000)

            label = punch_btn.inner_text()
            print("Detected:", label)

            punch_btn.click()

            page.wait_for_timeout(3000)

            # success screenshot
            page.screenshot(path="screenshot.png", full_page=True)

            print("Attendance marked ✓")

        except Exception as e:
            print("ERROR:", e)

            # failure screenshot
            page.screenshot(path="screenshot.png", full_page=True)

            raise e

        finally:
            browser.close()


if __name__ == "__main__":
    run()

