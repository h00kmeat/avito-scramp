import requests
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
import aiohttp
import asyncio
import time
import random
from aiohttp_proxy import ProxyConnector
from middlewares.states import UserState
import aiohttp_socks

proxies = {
    "https": "http://85860d734d:60e3dc1585@95.31.211.120:40292",
    "http": "http://77a26ef3d1:75d1761627@109.195.6.234:40050",
    # "socks5://user140068:cy4i8q@185.81.147.63:19885",
    # "http://45.8.211.113:80",
    # "http://185.221.160.60:80",
    # "http://62.33.207.201:3128",
    # "http://95.66.138.21:8880",
    # "http://185.221.160.176:80",
    # "http://185.174.138.19:80",
    # "http://185.221.160.60:80",
    # "http://45.8.211.64:80",
}
current_proxy_index = 0
router = Router()


# async def fetch_with_proxy(url, proxy):
#     connector = ProxyConnector.from_url(proxy)
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
#         "Referer": "https://www.avito.ru/",
#     }
#     async with aiohttp.ClientSession(connector=connector) as session:
#         async with session.get(url, headers=headers) as response:
#             print(response)
#             return await response.text()
#


@router.message(
    UserState.waiting_to_be_created, lambda message: message.text.startswith("http")
)
async def handle_item_link(message: types.Message, state: FSMContext):
    link = message.text
    # for proxy in proxies:
    req = requests.get(link)
    print(req.status_code)
    # print(proxy)
    # sleep_time = random.uniform(1, 10)
    # await asyncio.sleep(sleep_time)
    # await fetch_with_proxy(link, proxy)
