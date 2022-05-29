import json

from database.async_db import AsyncDatabase
from flask import Flask, render_template

app = Flask(__name__)
# app.secret_key = os.urandom(12)  # Generic key for dev purposes only
db = AsyncDatabase()


@app.route('/test', methods=['GET'])
async def test():
    return {}


@app.route('/test_basic_db', methods=['GET'])
async def test_basic_db():
    data = await db.get_data_by_id()
    return data.to_dict()


@app.route('/test_medium_db', methods=['GET'])
async def test_medium_db():
    return json.dumps([obj.to_dict() for obj in await db.get_data_by_like()])


@app.route('/test_wait_db', methods=['GET'])
async def test_wait_db():
    await db.sleep()
    return {}


@app.route('/test_basic_html', methods=['GET'])
async def test_basic_html():
    return render_template('index.html')


@app.route('/test_large_html', methods=['GET'])
async def test_large_html():
    data = await db.get_random_data(100)
    return render_template('index_render.html', data=data)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=8080)
