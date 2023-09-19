import requests
import threading
from app import app
from io import BytesIO
from decouple import config
from flask_mail import Message
from flask import render_template, request, current_app, flash, url_for, redirect, send_file

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/download", methods=['GET'])
def download():
    try:
        url = config('RESUME_URL')
        response = requests.get(url)
        if response.status_code == 200:
            file_content = response.content
            file_name = "resume-deba.pdf"
            return send_file(
                BytesIO(file_content),
                as_attachment=True,
                download_name=file_name,
                mimetype="application/pdf"
            )
        else:
            flash("Unable to get resume.")
            return redirect(url_for('home'))
    except Exception as e:
        flash(f"Unable to get resume.")
        return redirect(url_for('home'))

def send_email(name, email, message):
    with app.app_context():
        recipients = config('RECIPIENTS').split(',')
        msg = Message(
            f"Message from {name} via portfolio",
            sender=email,
            recipients=recipients
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

        if config('DEPLOYMENT') == "vercel":
            send_email(name, email, message)
        else:
            send_email_thread = threading.Thread(
                target=send_email, args=(name, email, message))
            send_email_thread.start()

        flash("Message sent successfully")
        return redirect(url_for('contact'))
    return render_template("contact.html")
