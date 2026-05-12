from utils.ai_healing import safe_locator


class LoginPage:

    def __init__(self, page):
        self.page = page

    def open_login(self):
        # Close welcome banner
        safe_locator(self.page, "text=Dismiss").click()

        # Open account menu
        safe_locator(
            self.page,
            "button[aria-label='Show/hide account menu']"
        ).click()

        self.page.get_by_role("menuitem", name="Go to login page").click()

    def enter_email(self, email):
        safe_locator(self.page, "#email").fill(email)

    def enter_password(self, password):
        safe_locator(self.page, "#password").fill(password)

    def click_login(self):
        safe_locator(self.page, "#loginButton").click()

    def login(self, email, password):
        self.open_login()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
