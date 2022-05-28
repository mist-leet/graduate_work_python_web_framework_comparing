#!/usr/bin/env bash

gunicorn app:get_app -w $1 --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker --chdir $2 --pythonpath aiohttp