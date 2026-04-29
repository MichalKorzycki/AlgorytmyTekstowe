# https://proxiesapi-com.medium.com/asynchronous-web-scraping-with-python-aiohttp-and-asyncio-83916022def7

import asyncio
from timeit import default_timer
from aiohttp import ClientSession, TCPConnector


def fetch_async(urls):
    start_time = default_timer()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(fetch_all(urls))
    loop.run_until_complete(future)
    tot_elapsed = default_timer() - start_time
    print()
    print(f'Total time taken : {str(tot_elapsed)}')


async def fetch_all(urls):
    tasks = []
    fetch.start_time = dict()

    # Proxy/Env settings for internal SE network
    async with ClientSession(trust_env=True, connector=TCPConnector(ssl=False)) as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        _ = await asyncio.gather(*tasks)

fetch_time = 0.0

async def fetch(url, session):
    global fetch_time
    fetch.start_time[url] = default_timer()
    async with session.get(url) as response:
        r = await response.read()
        elapsed = default_timer() - fetch.start_time[url]
        fetch_time += elapsed
        print(f'{url} took {str(elapsed)}')
        return r


if __name__ == '__main__':
    urls = ['https://nytimes.com',
            'https://github.com',
            'https://google.com',
            'https://reddit.com',
            'https://producthunt.com']
    fetch_async(urls)
    print(f'Total fetch time : {str(fetch_time)}')