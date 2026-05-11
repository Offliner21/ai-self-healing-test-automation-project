import allure

from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage

from utils.config import BASE_URL, TEST_EMAIL, TEST_PASSWORD


@allure.feature("Authentication")
@allure.story("Valid Login")
def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(BASE_URL)

        allure.attach(
            page.screenshot(),
            name="homepage",
            attachment_type=allure.attachment_type.PNG
        )

        login_page = LoginPage(page)

        login_page.login(TEST_EMAIL, TEST_PASSWORD)

        allure.attach(
            page.screenshot(),
            name="after-login",
            attachment_type=allure.attachment_type.PNG
        )

        assert page.locator(
            "button[aria-label='Show/hide account menu']"
        ).is_visible()

        browser.close()
