import openai
from utils.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def ai_heal_selector(failed_selector, page_html):
    prompt = f"""
    The selector '{failed_selector}' failed.
    Here is the page HTML:
    {page_html[:2000]}

    Suggest a new valid Playwright selector.
    Return only the selector.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content'].strip()


def safe_locator(page, selector):
    try:
        return page.locator(selector)
    except Exception:
        print(f"[AI HEALING] Failed selector: {selector}")

        html = page.content()
        new_selector = ai_heal_selector(selector, html)

        print(f"[AI HEALING] New selector: {new_selector}")

        return page.locator(new_selector)
