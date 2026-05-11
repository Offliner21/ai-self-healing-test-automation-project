import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:3000"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_OS")

TEST_EMAIL = os.getenv("TEST_EMAIL_OS")
TEST_PASSWORD = os.getenv("TEST_PASSWORD_OS")

SNYK_TOKEN = os.getenv("SNYK_API_KEY_OS")
