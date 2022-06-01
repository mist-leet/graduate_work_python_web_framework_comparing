#!/usr/bin/env bash

gunicorn app:app -w $1 --bind localhost:8080 -k uvicorn.workers.UvicornWorker --chdir $2 --pythonpath fastAPI