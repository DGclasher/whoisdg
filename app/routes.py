from app import app
from flask import render_template, request, current_app

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/projects")
def projects():
    projects = current_app.db.get_projects()
    return render_template("projects.html", projects=projects)

@app.route("/contact", methods=['GET','POST'])
def contact():
    emailSender = current_app.email_sender
    if request.method == 'POST':
        name = str(request.form.get('name'))
        email = str(request.form.get('email'))
        message = str(request.form.get('message'))
        is_sent = emailSender.message_handler(name, email, message)
        if is_sent:
            message = "Message sent sucessfully"
        else:
            message = "There was an error sending the message"
        return render_template("contact.html", message=message, is_sent=is_sent)
    return render_template("contact.html")


