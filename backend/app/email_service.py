import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_NAME = os.getenv("FROM_NAME", "Support")

def send_email(to_email: str, subject: str, content: str) -> bool:
    if not SENDGRID_API_KEY:
        print("❌ SENDGRID_API_KEY missing")
        return False

    try:
        message = Mail(
            from_email=(FROM_EMAIL, FROM_NAME),
            to_emails=to_email,
            subject=subject,
            plain_text_content=content
        )

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        print("✅ Email sent via SendGrid | status:", response.status_code)
        return True

    except Exception as e:
        print("❌ SendGrid error:", e)
        return False
