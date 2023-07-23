import secrets
from flask import Flask
from controllers.db import Database
from controllers.email_sender import EmailSender

app = Flask(__name__, static_folder="./static", static_url_path="/static")
app.secret_key = secrets.token_hex(16)
app.email_sender = EmailSender()
app.db = Database()

from app import routes