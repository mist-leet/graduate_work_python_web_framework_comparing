import os
import random
import string
from typing import List

from dotenv import load_dotenv
from sqlalchemy import Integer, Column, String
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database
from sqlalchemy_utils.functions import database_exists

load_dotenv()

Base = declarative_base()


def get_default_string() -> str:
    alphabet = string.ascii_lowercase[:10]
    return ''.join([random.choice(alphabet) for c in range(255)])


def get_random_search_pattern() -> str:
    alphabet = string.ascii_lowercase[:10]
    return '%' + ''.join([random.choice(alphabet) for c in range(7)]) + '%'


class SimpleMock(Base):
    __tablename__ = 'simplemock'

    id = Column(Integer(), primary_key=True, autoincrement=True, unique=True)
    text = Column(String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
        }


class SyncDatabase:
    SIMPLE_MOCK_ROW_COUNT = 1_000_000

    def __init__(self):
        self.db_user = os.getenv('POSTGRES_USER') or 'admin'
        self.db_password = os.getenv('POSTGRES_PASSWORD') or 'admin'
        self.db_ip = os.getenv('POSTGRES_IP') or 'localhost'
        self.db_name = os.getenv('POSTGRES_DB') or 'test'
        self.db_port = os.getenv('DB_PORT') or '5432'

        # formatting
        self.db_host = os.getenv('PG_HOSTNAME') or 'localhost'
        self.engine = create_engine(
            f'postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}',
            echo=False,
        )
        # drop_database(self.engine.url)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        Base.metadata.create_all(self.engine, checkfirst=True)
        self.session = Session(bind=self.engine)

    def generate_data(self) -> None:
        i = 0
        chunk_size = 10_000
        while i != self.SIMPLE_MOCK_ROW_COUNT:
            objects = [
                SimpleMock(text=get_default_string()) for j in range(chunk_size)
            ]
            i += chunk_size
            print(f'{i} objects generated', end=' ')
            self.session.add_all(objects)
            self.session.commit()
            print(f'{i} objects commited')

    def get_data_by_id(self) -> SimpleMock:
        return (
            self.session
                .query(SimpleMock)
                .filter(SimpleMock.id == random.randint(0, self.SIMPLE_MOCK_ROW_COUNT))
                .first()
        )

    def get_data_by_like(self) -> List[SimpleMock]:
        return (
            self.session
                .query(SimpleMock)
                .filter(SimpleMock.text.like(get_random_search_pattern()))
                .all()
        )

    def get_random_data(self, n: int) -> List[SimpleMock]:
        return (
            self.session
                .query(SimpleMock)
                .limit(n)
                .all()
        )

    def sleep(self):
        with self.engine.connect() as con:
            con.execute(text('select pg_sleep(2);'))
            return True


class AsyncDatabase:
    SIMPLE_MOCK_ROW_COUNT = 1_000_000

    def __init__(self):
        self.db_user = os.getenv('POSTGRES_USER') or 'admin'
        self.db_password = os.getenv('POSTGRES_PASSWORD') or 'admin'
        self.db_ip = os.getenv('POSTGRES_IP') or 'localhost'
        self.db_name = os.getenv('POSTGRES_DB') or 'test'
        self.db_port = os.getenv('DB_PORT') or '5432'

        self.db_host = os.getenv('PG_HOSTNAME') or 'localhost'

        self.engine = create_async_engine(
            f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}',
            echo=False,
        )
        self.async_session = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def generate_data(self) -> None:
        i = 0
        chunk_size = 10_000
        while i != self.SIMPLE_MOCK_ROW_COUNT:
            async with self.async_session() as session:
                objects = [
                    SimpleMock(text=get_default_string()) for j in range(chunk_size)
                ]
                i += chunk_size
                print(f'{i} objects generated', end=' ')
                session.add_all(objects)
                session.commit()
                print(f'{i} objects commited')

    async def get_data_by_id(self) -> SimpleMock:
        async with self.async_session() as session:
            query = select(SimpleMock).where(SimpleMock.id == random.randint(0, self.SIMPLE_MOCK_ROW_COUNT))
            return (await session.execute(query)).scalars().first()

    async def get_random_data(self, n: int) -> List[SimpleMock]:
        async with self.async_session() as session:
            query = select(SimpleMock).limit(n)
            return (await session.execute(query)).scalars().all()

    async def get_data_by_like(self) -> List[SimpleMock]:
        async with self.async_session() as session:
            query = select(SimpleMock).where(SimpleMock.text.like(get_random_search_pattern()))
            return (await session.execute(query)).scalars().all()

    async def sleep(self):
        async with self.engine.connect() as conn:
            await conn.execute(text('select pg_sleep(2);'))
            return True
