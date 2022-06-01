import json
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles
from api import router

app = fastapi.FastAPI()


def configure():
    configure_routing()


def configure_routing():
    app.mount('/static', StaticFiles(directory='../static/basic'), name='static')
    app.include_router(router)


if __name__ == '__main__':
    configure()
    # uvicorn.run(api, port=8080, host='127.0.0.1')