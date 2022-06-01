#!/usr/bin/env bash

gunicorn app:app -w $1 --bind localhost:8080 --chdir $2 --pythonpath flask