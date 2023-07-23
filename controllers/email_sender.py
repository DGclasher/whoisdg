import smtplib
from decouple import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self):
        self.email = config("EMAIL")
        self.passwd = config("PASS")
        self.official_email = "debaghosh1603@gmail.com"
        self.initialize()

    def initialize(self):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login(self.email, self.passwd)

    def message_handler(self, name, email, message):
        if message:
            msg = MIMEMultipart()
            msg['from'] = email
            msg['to'] = self.official_email
            msg['subject'] = f"Contact from {name}"
            msg.attach(MIMEText(message, 'plain'))
            self.send_email(msg.as_string())
        else:
            return 0

    def send_email(self, message):
        try:
            self.server.sendmail(self.email, self.official_email, message)
            self.server.quit()
            return 1
        except Exception as e:
            print(e)
            return 0
        