FROM python:3.11-alpine

RUN mkdir /app
COPY . /app/
WORKDIR /app

RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh

CMD [ "/app/entrypoint.sh" ]
