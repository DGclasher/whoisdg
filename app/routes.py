import threading
from app import app
from flask import render_template, request, current_app, flash, url_for, redirect


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/projects")
def projects():
    return "Work in progress"


def send_email_async(emailSender, name, email, message):
    with app.app_context():
        emailSender.message_handler(name, email, message)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    email_thread = threading.Thread(target=current_app.email_sender.initialize)
    email_thread.start()
    if request.method == 'POST':
        name = str(request.form.get('name'))
        email = str(request.form.get('email'))
        message = str(request.form.get('message'))

        email_send_thread = threading.Thread(target=send_email_async, args=(
            current_app.email_sender, name, email, message))
        email_send_thread.start()
        flash("Message sent successfully")
        return redirect(url_for('contact'))
    return render_template("contact.html")
