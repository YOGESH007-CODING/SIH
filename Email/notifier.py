import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

from Email.template_generator import Email_template
from datetime import datetime


# Load .env variables
load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

class Email_notifier():
    def __init__(self):
        pass
    def send_mail(self, state):
        if state['approvals']["authority_review"]!= True:
            print(f"The issue status is {state['review_status']}")
            return
        email_status={'status': 'pending', 'timestamp': None}
        # Create email object
        Subject, Body=Email_template(state)
        image_paths=state['image_paths']
        msg = MIMEMultipart("related")
        msg["From"] = EMAIL_HOST_USER
        Emails=state['Authority_info']['Email']
        # msg["To"] = Emails['Main']
        msg["To"] = "chaitanya.vashisth1@gmail.com"
        # msg['Cc']= Emails['cc']
        msg["Subject"] = Subject

        msg_alternative = MIMEMultipart("alternative")
        msg.attach(msg_alternative)

        # Attach HTML body
        msg_alternative.attach(MIMEText(Body, "html"))

        # Attach image
        # with open(image_path, "rb") as img_file:
        #     img = MIMEImage(img_file.read())
        #     img.add_header("Content-ID", "<issue_photo>")
        #     img.add_header("Content-Disposition", "inline", filename="evidence.jpg")
        #     msg.attach(img)

        max_images = 5
        for i, image_path in enumerate(image_paths[:min(len(image_paths), max_images)]):
            with open(image_path, "rb") as img_file:
                img = MIMEImage(img_file.read())
                img.add_header("Content-ID", f"<issue_photo_{i}>")
                img.add_header("Content-Disposition", "inline", filename=f"evidence_{i + 1}.jpg")
                msg.attach(img)

        # Send email
        try:
            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(msg)
            server.quit()
            email_status['status']="Completed"
            now = datetime.now()
            email_status['timestamp']=str(now)
            print("✅ Email with embedded image sent successfully.")

        except Exception as e:
            email_status['status'] = "Failed"
            now = datetime.now()
            email_status['timestamp'] = str(now)
            print(f"❌ Failed to send email: {e}")
        return email_status


