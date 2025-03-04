import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER") or ""
SMTP_PORT = os.getenv("SMTP_PORT", "456")
SENDER_EMAIL = os.getenv("SENDER_EMAIL") or ""
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD") or ""
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL") or ""
PAGE_URL = os.getenv("PAGE_URL") or ""
DATABASE_URL = os.getenv("DATABASE_URL") or ""