import asyncio
import os
import pytest
import pytest_asyncio
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


# pytest-asyncioのevent_loopを上書きする
# 変更点：関数スコープ→テストセッションスコープ）
@pytest.fixture(scope='session')
def event_loop():
    """pytest-asyncioで使用するasyncio.event_loop
        pytest-asyncioの標準のevent_loopを上書きすることで
        関数スコープ→テストセッションスコープへと変更
        これにより全テストでDBセッションが複数回発生しない

    Yields:
        _type_: _description_
    """

    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_db_session() -> AsyncSession:
    """pytestの時に使用するDBセッション

    Yields:
        AsyncSession: _description_
    """
    async with AsyncTestDbSession() as session:
        yield session
