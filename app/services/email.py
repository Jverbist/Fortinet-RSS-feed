import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL, RECIPIENT_EMAIL
import logging

logger = logging.getLogger(__name__)

async def send_email(subject: str, bulletin_id: str, title: str, link: str, published: str, color: str):
    """Send email notification for new RSS entry via SMTP"""
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        logger.warning("SMTP credentials not set. Email not sent.")
        return False
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: {color}; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <p style="color: white; margin: 0; font-weight: bold; font-size: 18px;">{bulletin_id}</p>
        </div>
        <h2 style="color: #212529; margin-top: 0;">{title}</h2>
        <p style="color: #6c757d; font-size: 14px;">Published: {published}</p>
        <div style="margin-top: 20px;">
            <a href="{link}" style="display: inline-block; background-color: #0d6efd; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">
                View Full Bulletin
            </a>
        </div>
        <hr style="border: none; border-top: 1px solid #e9ecef; margin: 30px 0;">
        <p style="color: #6c757d; font-size: 12px; margin: 0;">
            RSS Feed Platform © 2024 - Fortinet Security Bulletins
        </p>
    </div>
    """
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        
        msg.attach(MIMEText(html_content, 'html'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent for {bulletin_id} to {RECIPIENT_EMAIL}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False
