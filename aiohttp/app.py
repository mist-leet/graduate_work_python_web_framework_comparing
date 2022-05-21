import asyncio
import os
from typing import Dict, List

from aiohttp import web

from database.async_db import AsyncDatabase, SyncDatabase, SimpleMock
import aiohttp_jinja2
import jinja2


class AiohttpApplication:

    def __init__(self, async_db: bool = False, run_app: bool = False) -> None:
        self.db = AsyncDatabase() if async_db else SyncDatabase()
        self.app = web.Application()
        aiohttp_jinja2.setup(
            self.app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "static"))
        )
        self.app['static_root_url'] = '/static'

        if async_db:
            self.app.add_routes([
                web.get('/test', self.test),
                web.get('/test_basic_html', self.test_basic_html),
                web.get('/test_large_html', self.test_large_html_async),
                web.get('/test_medium_db', self.test_medium_db_async),
                web.get('/test_basic_db', self.test_basic_db_async),
                web.get('/test_complex_db', self.test_complex_db),
                web.get('/test_wait_db', self.test_wait_db_async),
            ])
        else:
            self.app.add_routes([
                web.get('/test', self.test),
                web.get('/test_basic_html', self.test_basic_html),
                web.get('/test_large_html', self.test_large_html),
                web.get('/test_medium_db', self.test_medium_db),
                web.get('/test_basic_db', self.test_basic_db),
                web.get('/test_complex_db', self.test_complex_db),
                web.get('/test_wait_db', self.test_wait_db),
            ])

        # STATIC_PATH = os.path.join(os.path.dirname(__file__), "../static")
        STATIC_PATH = '/home/ilya/git/graduate_work_python_web_framework_comparing/static/basic/'
        self.app.router.add_static('/static/', STATIC_PATH, name='static')

        if run_app:
            web.run_app(self.app)

    async def get_app(self):
        return self.app

    async def test(self, request: web.Request) -> web.Response:
        return web.Response(text='200 OK')

    @aiohttp_jinja2.template("basic/index.html")
    async def test_basic_html(self, request: web.Request) -> Dict:
        return {}

    @aiohttp_jinja2.template("basic/index_render.html")
    async def test_large_html(self, request: web.Request) -> Dict[str, List[SimpleMock]]:
        return {'data': self.db.get_random_data(100)}

    @aiohttp_jinja2.template("basic/index_render.html")
    async def test_large_html_async(self, request: web.Request) -> Dict[str, List[SimpleMock]]:
        return {'data': await self.db.get_random_data(100)}

    async def test_basic_db(self, request: web.Request) -> web.Response:
        data = self.db.get_data_by_id()
        return web.json_response(data=data.to_dict())

    async def test_medium_db(self, request: web.Request) -> web.Response:
        data = [obj.to_dict() for obj in self.db.get_data_by_like()]
        return web.json_response(data=data)

    async def test_basic_db_async(self, request: web.Request) -> web.Response:
        data = await self.db.get_data_by_id()
        return web.json_response(data=data.to_dict())

    async def test_medium_db_async(self, request: web.Request) -> web.Response:
        data = [obj.to_dict() for obj in await self.db.get_data_by_like()]
        return web.json_response(data=data)

    async def test_complex_db(self, request: web.Request) -> web.Response:
        return web.Response()

    async def test_wait_db(self, request: web.Request) -> web.Response:
        self.db.sleep()
        return web.Response()

    async def test_wait_db_async(self, request: web.Request) -> web.Response:
        await self.db.sleep()
        return web.Response()


async def get_app():
    app_obj = AiohttpApplication(
        async_db=True,
        run_app=False
    )
    return await app_obj.get_app()


if __name__ == '__main__':
    asyncio.run(get_app())
