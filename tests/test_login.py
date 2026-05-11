from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from utils.config import BASE_URL, TEST_EMAIL,TEST_PASSWORD,SNYK_TOKEN


def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(BASE_URL)

        login_page = LoginPage(page)
        login_page.login(TEST_EMAIL, TEST_PASSWORD)

        assert page.locator("text= OWASP Juice Shop").nth(2).is_visible()

        browser.close()