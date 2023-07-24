import threading
from app import app
from flask_mail import Message
from flask import render_template, request, current_app, flash, url_for, redirect


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/projects")
def projects():
    return "Work in progress"


def send_email(name, email, message):
    with app.app_context():
        msg = Message(
            f"Message from {name} via portfolio",
            sender=email,
            recipients=["debaghosh1603@gmail.com"]
        )
        msg.body = message
        msg.body += f"\n\nFrom: {email}"
        current_app.mail.send(msg)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = str(request.form.get('name'))
        email = str(request.form.get('email'))
        message = str(request.form.get('message'))

        send_email_thread = threading.Thread(
            target=send_email, args=(name, email, message))
        send_email_thread.start()

        flash("Message sent successfully")
        return redirect(url_for('contact'))
    return render_template("contact.html")
