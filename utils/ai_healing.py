import time

from colorama import Fore, init

from utils.llm_healing import ask_llm_for_locator

init(autoreset=True)


def slow_print(message, color=Fore.CYAN, delay=0.02):
    for char in message:
        print(color + char, end="", flush=True)
        time.sleep(delay)

    print()


FALLBACK_CANDIDATES = {

    "text=Account": [

        "button[aria-label='Show/hide account menu']",

        "button:has-text('Account')",

        "[aria-label='Show/hide account menu']"
    ],

    "text=Login": [

        "button[aria-label='Go to login page']",

        "button:has-text('Login')"
    ],

    "#broken_email": [

        "#email",

        "input[aria-label='Email']",

        "input[type='email']",

        "input[type='text']"
    ],

    "#broken_password": [

        "#password",

        "input[aria-label='Password']",

        "input[type='password']"
    ],

    "#broken_loginButton": [

        "#loginButton",

        "button[type='submit']",

        "button:has-text('Log in')"
    ]
}


def validate_locator(page, selector):
    try:

        locator = page.locator(selector)

        count = locator.count()

        if count == 0:
            return None

        locator.first.wait_for(
            timeout=5000,
            state="visible"
        )

        return locator.first

    except Exception:

        return None


def safe_locator(page, selector):
    slow_print(
        f"\n[AI ENGINE] Attempting locator -> {selector}",
        Fore.CYAN
    )

    try:

        locator = page.locator(selector)

        locator.wait_for(timeout=3000)

        slow_print(
            "[SUCCESS] Locator resolved successfully",
            Fore.GREEN
        )

        return locator

    except Exception:

        slow_print(
            "\n[WARNING] Locator failure detected",
            Fore.YELLOW
        )

        slow_print(
            "[AI] Extracting live DOM...",
            Fore.MAGENTA
        )

        dom = page.content()

        time.sleep(1)

        slow_print(
            "[AI] Sending DOM + failed locator to LLM...",
            Fore.BLUE
        )

        time.sleep(1)

        healed_selector = ask_llm_for_locator(
            dom,
            selector
        )

        slow_print(
            "\n[LLM RESPONSE]",
            Fore.CYAN
        )

        slow_print(
            f"Failed locator : {selector}",
            Fore.RED
        )

        slow_print(
            f"Suggested fix  : {healed_selector}",
            Fore.GREEN
        )

        slow_print(
            "\n[AI VALIDATION] Verifying LLM locator...",
            Fore.YELLOW
        )

        page.wait_for_timeout(2000)

        validated = validate_locator(
            page,
            healed_selector
        )

        if validated:
            slow_print(
                "[AI VALIDATION] LLM locator valid",
                Fore.GREEN
            )

            slow_print(
                "\n[AI HEALING] Recovery successful",
                Fore.GREEN
            )

            slow_print(
                "[FRAMEWORK] Retrying test execution...",
                Fore.CYAN
            )

            return validated

        slow_print(
            "\n[AI VALIDATION] LLM locator failed",
            Fore.RED
        )

        slow_print(
            "[FALLBACK ENGINE] Trying smart candidates...",
            Fore.YELLOW
        )

        candidates = FALLBACK_CANDIDATES.get(
            selector,
            []
        )

        for candidate in candidates:

            slow_print(
                f"[CANDIDATE] Testing -> {candidate}",
                Fore.CYAN
            )

            validated = validate_locator(
                page,
                candidate
            )

            if validated:
                slow_print(
                    f"[SUCCESS] Candidate matched -> {candidate}",
                    Fore.GREEN
                )

                slow_print(
                    "\n[AI HEALING] Recovery successful",
                    Fore.GREEN
                )

                slow_print(
                    "[FRAMEWORK] Retrying test execution...",
                    Fore.CYAN
                )

                return validated

        raise Exception(
            f"No valid healing locator found for: {selector}"
        )
