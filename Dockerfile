FROM python:3.13.0a4-alpine

RUN mkdir /app
COPY . /app/
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "gunicorn", "--worker-tmp-dir", "/dev/shm", "-w", "2", "--bind", "0.0.0.0:5000", "app:app" ]
