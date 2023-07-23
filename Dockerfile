FROM python:3.11-bullseye

WORKDIR /whoisdg

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY . /whoisdg

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "app:app" ]
