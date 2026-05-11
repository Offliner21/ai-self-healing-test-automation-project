from behave import given, when, then
from pages.login_page import LoginPage
from utils.config import BASE_URL, TEST_EMAIL, TEST_PASSWORD
from utils.ai_healing import safe_locator


@given('the Juice Shop login page is open')
def step_open_login_page(context):
    context.page.goto(BASE_URL)

    # Dismiss popup
    safe_locator(context.page, "text=Dismiss").click()

    # Open account menu
    safe_locator(context.page, "text=Account").nth(2).click()

    # Open login page
    context.page.get_by_role(
        "menuitem",
        name="Go to login page"
    ).click()

    context.login_page = LoginPage(context.page)


@when('the user enters valid credentials')
def step_enter_credentials(context):
    context.login_page.enter_email(TEST_EMAIL)

    context.login_page.enter_password(TEST_PASSWORD)


@when('clicks the login button')
def step_click_login(context):
    context.login_page.click_login()


@then('the user should be logged in successfully')
def step_validate_login(context):
    assert context.page.get_by_role(
        "button",
        name="Back to homepage"
    ).is_visible()
