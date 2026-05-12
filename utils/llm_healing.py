from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY_OS")
)


def clean_dom(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "svg", "path"]):
        tag.decompose()

    important = []

    candidates = soup.find_all([
        "input",
        "button",
        "a",
        "span"
    ])

    for element in candidates:

        attrs = []

        if element.get("id"):
            attrs.append(f"id='{element.get('id')}'")

        if element.get("name"):
            attrs.append(f"name='{element.get('name')}'")

        if element.get("type"):
            attrs.append(f"type='{element.get('type')}'")

        if element.get("placeholder"):
            attrs.append(
                f"placeholder='{element.get('placeholder')}'"
            )

        if element.get("aria-label"):
            attrs.append(
                f"aria-label='{element.get('aria-label')}'"
            )

        text = element.get_text(strip=True)

        if text:
            attrs.append(f"text='{text}'")

        important.append(
            f"<{element.name} {' '.join(attrs)}>"
        )

    return "\n".join(important[:120])


def ask_llm_for_locator(dom, failed_locator):
    cleaned_dom = clean_dom(dom)

    prompt = f"""
You are an AI QA automation healing engine.

A Playwright locator failed.

FAILED LOCATOR:
{failed_locator}

AVAILABLE PAGE ELEMENTS:
{cleaned_dom}

TASK:
Find the BEST Playwright CSS selector replacement.

RULES:
- Return ONLY ONE selector
- Prefer IDs first
- Then aria-label
- Then placeholder
- Then text
- NEVER explain
- NEVER use XPath
- ONLY return the selector

GOOD EXAMPLES:
#email
#password
#loginButton
button[aria-label='Show/hide account menu']
input[placeholder='Email']
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert Playwright locator healing AI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    selector = response.choices[0].message.content.strip()

    print("\n[LLM RAW RESPONSE]")
    print(selector)

    return selector
