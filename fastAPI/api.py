import fastapi
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from database.async_db import AsyncDatabase

router = fastapi.APIRouter()
templates = Jinja2Templates('../static/basic')
db = AsyncDatabase()


@router.get('/test')
async def test():
    return {}


@router.get('/test_basic_db')
async def test_basic_db():
    data = await db.get_data_by_id()
    return data.to_dict()


@router.get('/test_medium_db')
async def test_medium_db():
    return [obj.to_dict() for obj in await db.get_data_by_like()]


@router.get('/test_wait_db')
async def test_wait_db():
    await db.sleep()
    return {}


@router.get('/test_basic_html')
async def test_basic_html(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/test_large_html')
async def test_large_html(request: Request):
    data = await db.get_random_data(100)
    return templates.TemplateResponse('index_render.html', {'data': data, 'request': request})
