import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from backend.config import settings

logger = logging.getLogger("EmailService")

def send_verification_email(email: str, user_name: str, token: str) -> dict:
    """
    Dispatches an email verification link to the user.
    - If SMTP is configured, sends a real HTML email.
    - Otherwise, logs the link clearly to the console for local development & testing.
    """
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    # 1. Attempt Real SMTP Delivery if credentials exist
    if settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Verify Your Email Address - CareerPath AI"
            msg["From"] = settings.SMTP_FROM or settings.SMTP_USER
            msg["To"] = email

            text_body = f"""Hello {user_name},

Thank you for registering on CareerPath AI!
Please click the link below to verify your email address and activate your account:

{verification_url}

This link is valid for 30 minutes. If you did not create this account, please ignore this email.

Best regards,
CareerPath AI Team
"""

            html_body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; margin: 0; padding: 24px; }}
    .container {{ max-width: 560px; margin: 0 auto; background: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }}
    .header {{ background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%); padding: 32px 24px; text-align: center; color: #ffffff; }}
    .content {{ padding: 32px 24px; color: #1e293b; line-height: 1.6; font-size: 15px; }}
    .btn {{ display: inline-block; background-color: #2563eb; color: #ffffff !important; text-decoration: none; padding: 13px 28px; border-radius: 10px; font-weight: 700; font-size: 15px; margin: 20px 0; text-align: center; }}
    .url-box {{ background: #f1f5f9; padding: 12px; border-radius: 8px; font-size: 12px; word-break: break-all; color: #475569; }}
    .footer {{ padding: 20px 24px; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #f1f5f9; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 style="margin: 0; font-size: 24px; font-weight: 800;">CareerPath AI</h1>
      <p style="margin: 6px 0 0 0; font-size: 13px; opacity: 0.9;">Intelligent Talent & Skill Ecosystem</p>
    </div>
    <div class="content">
      <h2 style="font-size: 18px; margin-top: 0; color: #0f172a;">Verify Your Email Address</h2>
      <p>Hello <strong>{user_name}</strong>,</p>
      <p>Thank you for signing up. Please verify your email address to activate your account and start benchmarking your skills against Indian industry roles.</p>
      <div style="text-align: center;">
        <a href="{verification_url}" class="btn">Verify Email & Activate Account</a>
      </div>
      <p style="font-size: 13px; color: #64748b;">Or copy and paste this verification URL into your browser:</p>
      <div class="url-box">{verification_url}</div>
      <p style="font-size: 12px; color: #e11d48; margin-top: 16px;">⏱️ This verification link expires in <strong>30 minutes</strong>.</p>
    </div>
    <div class="footer">
      If you did not request this account, you can safely ignore this email.<br>&copy; CareerPath AI Ecosystem
    </div>
  </div>
</body>
</html>
"""
            msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            logger.info(f"Verification email successfully delivered to {email} via SMTP")
            return {"sent": True, "method": "smtp", "verification_url": verification_url}
        except Exception as e:
            logger.error(f"SMTP email dispatch failed: {e}. Falling back to console dispatch.")

    # 2. Local / Development Fallback (Clear formatted console dispatch)
    banner = f"""
==================================================================
[CAREERPATH AI EMAIL SERVICE] VERIFICATION LINK DISPATCHED
==================================================================
To: {email}
Recipient: {user_name}
Verification URL: {verification_url}
Token: {token}
Expires In: 30 minutes
==================================================================
"""
    print(banner, flush=True)
    logger.info(f"Generated verification link for {email}: {verification_url}")
    return {"sent": True, "method": "console", "verification_url": verification_url}
