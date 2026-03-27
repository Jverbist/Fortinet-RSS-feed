import os
from dotenv import load_dotenv

load_dotenv()

# SMTP Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp")
SMTP_PORT = int(os.getenv("SMTP_PORT", "25"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "rss-update@rss.local")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "tech@exlcusive-networks.be")
RSS_CHECK_INTERVAL = int(os.getenv("RSS_CHECK_INTERVAL", "600"))  # 10 minutes in seconds
