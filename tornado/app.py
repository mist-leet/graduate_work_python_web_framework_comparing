import os
import sys
from dotenv import load_dotenv

load_dotenv('../database/.env')

sys.path.append(os.getenv('BASE_DIR'))
print(os.getenv('BASE_DIR'))


import json

import tornado.ioloop
import tornado.web
import tornado.wsgi

from database.async_db import AsyncDatabase


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('')


class TestBasicDbHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    async def get(self):
        data = await self.db.get_data_by_id()
        self.write(json.dumps(data.to_dict()))


class TestMediumDbDbHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    async def get(self):
        data = [obj.to_dict() for obj in await self.db.get_data_by_like()]
        self.write(json.dumps(data))


class TestWaitDbHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    async def get(self):
        await self.db.sleep()
        self.write('')


class TestBasicHtmlHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class TestLargeHtmlHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    async def get(self):
        data = await self.db.get_random_data(100)
        await self.render('index_render.html', data=data)


if __name__ == '__main__':
    db = AsyncDatabase()
    app = tornado.web.Application([
        (r'/test', TestHandler),
        (r'/test_basic_html', TestBasicHtmlHandler),
        (r'/test_large_html', TestLargeHtmlHandler, dict(db=db)),
        (r'/test_basic_db', TestBasicDbHandler, dict(db=db)),
        (r'/test_medium_db', TestMediumDbDbHandler, dict(db=db)),
        (r'/test_wait_db', TestWaitDbHandler, dict(db=db)),
    ],
        template_path=os.getenv('BASE_DIR') + '/static/tornado/',
        static_path=os.getenv('BASE_DIR') + '/static/tornado/',
    )
    app.listen(int(sys.argv[1]))
    tornado.ioloop.IOLoop.current().start()
