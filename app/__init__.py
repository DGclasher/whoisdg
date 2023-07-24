import secrets
from flask import Flask
from decouple import config
from flask_mail import Mail
from controllers.db import Database

app = Flask(__name__, static_folder="./static", static_url_path="/static")
app.secret_key = secrets.token_hex(16)
app.db = Database()

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = config("EMAIL")
app.config["MAIL_PASSWORD"] = config("PASS")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.mail = Mail(app)

from app import routes