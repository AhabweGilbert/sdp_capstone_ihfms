import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Initialize email settings here
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.smtp_username = '********'
        self.smtp_password = '********'

    def send_email(self, to_email, patient_id):
        try:
            # Create SMTP connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password) 

            print("Email sent successfully!")

            email_values = {
                'email_to': to_email,
                'email_cc': False,
                'auto_delete': True,
                'recipient_ids': [],
                'partner_ids': [],
                'scheduled_date': False,
                }
            with payment_data.env.cr.savepoint():
                email_template.with_context(**context).send_mail(
                    patient_id, force_send=True, raise_exception=True, email_values=email_values, email_layout_xmlid='mail.mail_notification_light'
                )
        except Exception as e:
            print("Error sending email:", str(e))

