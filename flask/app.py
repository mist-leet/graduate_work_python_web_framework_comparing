import json
import os

from database.async_db import SyncDatabase
from flask import Flask, render_template

app = Flask(
    __name__,
    static_folder=f'{os.getenv("BASE_DIR")}/static/flask/',
    static_url_path='/static',
    template_folder=f'{os.getenv("BASE_DIR")}/static/flask/',
)
print('Run with\t', f'{os.getenv("BASE_DIR")}/static')

db = SyncDatabase()

@app.route('/test', methods=['GET'])
async def test():
    return {}


@app.route('/test_basic_db', methods=['GET'])
async def test_basic_db():
    data = db.get_data_by_id()
    return data.to_dict()


@app.route('/test_medium_db', methods=['GET'])
async def test_medium_db():
    return json.dumps([obj.to_dict() for obj in db.get_data_by_like()])


@app.route('/test_wait_db', methods=['GET'])
async def test_wait_db():
    db.sleep()
    return {}


@app.route('/test_basic_html', methods=['GET'])
async def test_basic_html():
    return render_template('index.html')


@app.route('/test_large_html', methods=['GET'])
async def test_large_html():
    data = db.get_random_data(100)
    return render_template('index_render.html', data=data)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=8080)
