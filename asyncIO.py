import asyncio
import pathlib
import aiofiles
from aiohttp import ClientSession
import json
import xmltodict
import time


async def fetch_html(url, session, **kwargs):
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """
    resp = await session.request(method="GET", url=url, **kwargs)
    html = await resp.text()
    return html


async def parse(url, session: ClientSession, **kwargs) -> set:
    temp_list = []
    podcast_name = ""
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
        json_string = json.dumps(xmltodict.parse(html), indent=4)
        data = json.loads(json_string)
        podcast_name = data['rss']['channel']['title']
        podcast_detail = data['rss']['channel']['item']
        for item in podcast_detail:
            if isinstance(item, dict):
                date = item['pubDate']
            elif isinstance(podcast_detail, dict):
                date = podcast_detail['pubDate']
            else:
                print("Error in url: ", url)
                continue
            temp_list.append(date)
    except Exception as e:
        print("Exception: {}".format(e))
    output = {"title": podcast_name, "url": url, "dates": temp_list}
    return output


async def write_one(file, url, **kwargs):
    res = await parse(url=url, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        await f.write(json.dumps(res))
        await f.write(",")


async def bulk_crawl_and_write(file, urls, **kwargs):
    """Crawl & write concurrently to `file` for multiple `urls`."""
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                write_one(file=file, url=url, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time.time()
    here = pathlib.Path(__file__).parent

    urls = open('urls.json', 'r')
    urls = json.loads(urls.read())

    outpath = here.joinpath("url_dates.json")

    with open(outpath, "w") as outfile:
        outfile.write("[")

    asyncio.run(bulk_crawl_and_write(file=outpath, urls=urls))

    with open(outpath, "a") as outfile:
        outfile.write("]")

    print(f"Execution time of ask_user: {time.time() - start_time}s")
    print("Complete.")