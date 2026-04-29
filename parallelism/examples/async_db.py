import asyncio

import asyncpg


async def run():
    conn = await asyncpg.connect(user='julia', password='julia99',
                                 database='async_example', host='127.0.0.1')
    values = await conn.fetch(
        'SELECT * FROM mytable WHERE id = $1',
        10,
    )
    print(values)
    await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
