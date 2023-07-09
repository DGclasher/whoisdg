#!/bin/sh

gunicorn --chdir app -w 2 -b 0.0.0.0:5000 --threads 2 app:app