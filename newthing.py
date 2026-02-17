from playwright.sync_api import sync_playwright

URL = "https://hrms-420.netlify.app/"

EMAIL = "satyanarayana.arahinfotech@gmail.com"
PASSWORD = "123456789"

EMAIL_SELECTOR = 'input[type="email"]'
PASS_SELECTOR = 'input[type="password"]'
LOGIN_BTN = 'button[type="submit"]'


def run():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Opening site...")
        page.goto(URL, wait_until="domcontentloaded")

        print("Waiting for login form...")
        page.wait_for_selector(EMAIL_SELECTOR, timeout=60000)

        print("Typing credentials...")
        page.fill(EMAIL_SELECTOR, EMAIL)
        page.fill(PASS_SELECTOR, PASSWORD)

        print("Submitting login...")
        page.click(LOGIN_BTN)

        print("Waiting for Break button...")

        break_btn = page.get_by_role("button", name="Break", exact=True)
        break_btn.wait_for(state="visible", timeout=60000)

        print("Highlighting button...")
        break_btn.highlight()

        print("Clicking Break button...")
        break_btn.click()

        print("Waiting to confirm click...")
        page.wait_for_timeout(5000)


        print("Success ✓")
        browser.close()


if __name__ == "__main__":
    run()

