import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

if not BOT_TOKEN or not PAYMENT_PROVIDER_TOKEN or not GROUP_ID:
    raise ValueError("Проверьте все переменные в .env")