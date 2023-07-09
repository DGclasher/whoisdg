FROM python:3.11-bullseye

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD [ "gunicorn","-w","4","--bind","0.0.0.0:5000","app:app" ]
