import asyncio

async def hello():
    return "hello"

async def world():
    return "world"


async def f():
    print(await hello())
    print(await world())

# Python 3.7+
asyncio.run(f())