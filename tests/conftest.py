import asyncio
import os
import pytest
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from gbf import models

AsyncTestDbSession = None

@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    env_path = os.path.join(os.environ['CONFIG_FOLDER'], '.env.test')
    load_dotenv(override=True, dotenv_path=env_path)

    DBUSER = os.environ['DBTESTUSER']
    DBPASSWORD = os.environ['DBTESTPASSWORD']
    DBHOST = os.environ['DBTESTHOST']
    DBDATABASE = os.environ['DBTESTDATABASE']

    URL = f'postgresql+asyncpg://{DBUSER}:{DBPASSWORD}@{DBHOST}/{DBDATABASE}'
    engine = create_async_engine(URL, echo=False)
    global AsyncTestDbSession
    AsyncTestDbSession = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession
    )

    async def init_db():
        async with engine.begin() as conn:
            await models.init_db(conn)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())


@pytest.fixture(scope="session")
async def async_db_session():
    async with AsyncTestDbSession() as session:
        yield session
