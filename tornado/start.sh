#!/usr/bin/env bash

gunicorn -k tornado app:app --chdir /home/ilya/git/graduate_work_python_web_framework_comparing --pythonpath tornado --bind localhost:8080