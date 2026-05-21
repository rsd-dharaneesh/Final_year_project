import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["From"] = "PaypaI Security <alert@paypa1-secure.com>"
msg["To"] = "user@company.com"
msg["Reply-To"] = "attacker@gmail.com"
msg["Subject"] = "URGENT: Verify your account immediately"

msg.set_content("Your account is limited.")

msg.add_alternative(
    """
    <html>
      <body>
        <h3>Security Alert</h3>
        <p>Your account is limited.</p>
        <form>
          <input type="password" />
        </form>
        <a href="http://192.168.1.10/login">Verify Now</a>
      </body>
    </html>
    """,
    subtype="html"
)

smtp = smtplib.SMTP("localhost", 2525)
smtp.send_message(msg)
smtp.quit()

print("✅ Phishing email sent successfully")
