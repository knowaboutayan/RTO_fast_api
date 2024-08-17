import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dotenv
import os
import gen_text

dotenv.load_dotenv()


def send_email(*, receiver_email=[], subject="No subject", body="Null", body_type="plain"):
    # Establish SMTP connection
    try:

        print("::Connecting to SMTP...")
        SMTP_CONN = smtplib.SMTP(os.getenv('HOST'), int(os.getenv('PORT')))
        SMTP_CONN.starttls()
        print("::Connection successful::")

        print('::Login processing...')
        SMTP_CONN.login(os.getenv('SENDER_EMAIL'), os.getenv('SMTP_PASSWORD'))
        print('::Login successful::')

        for to_email in receiver_email:
            msg = MIMEMultipart()
            msg['From'] = os.getenv('SENDER_EMAIL')
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, body_type))
            SMTP_CONN.sendmail(os.getenv('SENDER_EMAIL'), to_email, msg.as_string())
            print(f"send_to:{to_email}")
            print('::Email successfully sent::')
    except Exception as err:
        print(f"{gen_text.ERR}{err}")
        print("::EMAIL NOT SEND::")
    else:
        SMTP_CONN.quit()
