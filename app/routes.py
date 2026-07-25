import re
import json
import os
import requests
import threading
import feedparser
from app import app
from io import BytesIO
from decouple import config
from flask_mail import Message
from urllib.request import ProxyHandler
from flask_paginate import Pagination
from flask import ( render_template,
                   request, current_app, 
                   flash, url_for, 
                   redirect, send_file )

@app.route("/")
def home():
    experiences = []
    exp_src = config('EXPERIENCE_SRC', default='tests/experience.json')
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    try:
        if isinstance(exp_src, str) and (exp_src.startswith('http://') or exp_src.startswith('https://')):
            try:
                resp = requests.get(exp_src, timeout=8)
                resp.raise_for_status()
                experiences = resp.json()
            except Exception as e:
                app.logger.error(f"Failed to fetch experiences from URL {exp_src}: {e}")
                experiences = []
        else:
            path = exp_src if os.path.isabs(exp_src) else os.path.join(base_dir, exp_src)
            with open(path, 'r') as f:
                experiences = json.load(f)
    except Exception as e:
        app.logger.error(f"Failed to load experiences: {e}")

    return render_template("home.html", experiences=experiences)

@app.route("/projects")
def projects():
    projects = []
    proj_src = config('PROJECTS_SRC', default='tests/sample_projects.json')
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    try:
        if isinstance(proj_src, str) and (proj_src.startswith('http://') or proj_src.startswith('https://')):
            try:
                resp = requests.get(proj_src, timeout=8)
                resp.raise_for_status()
                projects = resp.json()
            except Exception as e:
                app.logger.error(f"Failed to fetch projects from URL {proj_src}: {e}")
                projects = []
        else:
            path = proj_src if os.path.isabs(proj_src) else os.path.join(base_dir, proj_src)
            with open(path, 'r') as f:
                projects = json.load(f)
    except Exception as e:
        app.logger.error(f"Failed to load projects: {e}")

    return render_template("projects.html", projects=projects)

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

def get_summary(full_summary):
    summary = re.sub(r'<.*?>','',full_summary)
    words = summary.split(" ")
    if len(words) < 20:
        return summary + " ..."
    summary = ""
    summary = " ".join(words[i] for i in range(0, 50))
    summary += " ..."
    return summary

def get_proxy():
    res = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all')
    proxy = res.text.split('\r\n')
    return proxy

@app.route('/blogs', methods=['GET'])
def blogs():
    proxy = get_proxy()
    proxy_handler = ProxyHandler({'http': f"http://{proxy}"})
    rss_url = config('RSS_URL')
    feed = feedparser.parse(rss_url, handlers=[proxy_handler])
    # with open("./tests/sample_posts.json", "r") as f:
    #     feed = json.loads(f.read())
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page
    blogs = [{'title': entry['title'], 'author': entry['author'], 'summary': get_summary(entry['summary']),
                        'published': entry['published'], 'link': entry['link']} for entry in feed['entries']]
    total = len(blogs)
    total_pages = (total + per_page - 1) // per_page
    items_pagination = blogs[offset:offset+per_page]
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=total)
    return render_template('blogs.html', blogs=blogs, pagination=pagination, items=items_pagination, total_pages=total_pages)
    
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
