import os
import secrets
import smtplib
from flask import *

app = Flask(__name__, static_url_path="/static", static_folder="./static")
app.secret_key = secrets.token_hex(16)

def send_mail(email, passwd, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, passwd)
    

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, debug=False)
