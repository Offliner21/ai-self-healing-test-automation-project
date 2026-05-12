import os

from openai import OpenAI

from bs4 import BeautifulSoup

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY_OS")
)


def ask_llm_for_locator(dom, failed_locator):
    soup = BeautifulSoup(dom, "html.parser")

    cleaned_dom = soup.prettify()

    prompt = f"""
You are an expert Playwright automation engineer.

A Playwright locator failed.

Failed locator:
{failed_locator}

HTML DOM:
{cleaned_dom[:12000]}

Rules:
1. Suggest ONLY ONE Playwright locator
2. Locator MUST uniquely identify a clickable or visible element
3. Prefer:
   - aria-label
   - id
   - data-testid
   - button selectors
4. Avoid generic text locators
5. Avoid chained CSS unless necessary
6. Return ONLY the locator string
7. The locator must work with Playwright page.locator()

Good examples:
button[aria-label='Show/hide account menu']
#email
input[type='email']
button[aria-label='Go to login page']

Return ONLY the locator.
"""

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior QA automation engineer "
                    "specialized in Playwright locator recovery."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1
    )

    locator = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    locator = locator.replace("```", "")
    locator = locator.replace("css=", "")
    locator = locator.strip()

    print("\n[LLM RAW RESPONSE]")
    print(locator)

    return locator
