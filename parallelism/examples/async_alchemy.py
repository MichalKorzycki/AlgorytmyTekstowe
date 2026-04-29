import asyncio

from sqlalchemy import MetaData
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import select


def use_inspector(conn):
    inspector = inspect(conn)
    return inspector.get_table_names()


def use_meta(conn):
    meta = MetaData(bind=conn)
    meta.reflect()
    return meta.tables['mytable']


async def async_main():
    engine = create_async_engine(
        "postgresql+asyncpg://julia:julia99@localhost/async_example", echo=True,
    )

    async with engine.begin() as conn:
        # CAVEAT !!!
        tables = await conn.run_sync(use_inspector)
        print(tables)
        # CAVEAT !!!
        mytable = await conn.run_sync(use_meta)
        await conn.execute(
            mytable.insert(), [{"name": "somename1", "id": 5}, {"name": "somename0", "id": 6}]
        )

    async with engine.connect() as conn:
        # select a Result, which will be delivered with buffered
        # results
        result = await conn.execute(select(mytable).where(mytable.c.name == "somename1"))

        print(result.fetchall())

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


asyncio.run(async_main())
