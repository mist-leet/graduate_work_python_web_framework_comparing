#!/usr/bin/env bash

gunicorn app:get_app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker --chdir /home/ilya/git/graduate_work_python_web_framework_comparing --pythonpath aiohttp

#gunicorn app:app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker --chdir /home/ilya/git/graduate_work_python_web_framework_comparing