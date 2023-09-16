#!/bin/sh

APP_PORT=${FLASK_RUN_PORT:-5000}

/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm -w 2 --bind "0.0.0.0:${APP_PORT}" app:app
