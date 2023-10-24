from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
import aiohttp
import asyncio
import random
from bs4 import BeautifulSoup
from aiohttp_proxy import ProxyConnector
from middlewares.states import UserState
import aiohttp_socks
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker
from models.all_models import User, Task, Item

proxies = {
    "http://85860d734d:60e3dc1585@95.31.211.120:40292",
    "http://77a26ef3d1:75d1761627@109.195.6.234:40050",
    "socks5://user140068:cy4i8q@185.81.147.63:19885",
}
router = Router()


async def data_parser(response, engine, user_id, link):
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find("div", {"data-marker": "item"})
    name = (
        data.find("a", {"itemprop": "url"}).find("h3", {"itemprop": "name"}).get_text()
    )
    url = "https://www.avito.ru" + data.find("a", {"itemprop": "url"}).get("href")
    price = (
        data.find("p", {"data-marker": "item-price"}).find("span", {"class": ""}).text
    )
    time_adding = data.find("p", {"data-marker": "item-date"}).get_text()
    category = soup.find("div", {"class": "index-searchGeoWrapper-MFIhV"}).find(
        "input", {"data-marker": "search-form/suggest"}
    )
    print(url + "\n" + price + "\n" + time_adding + "\n")
    Session = sessionmaker(bind=engine)
    session = Session()
    task = (
        session.query(Task)
        .filter(Task.user_id == user_id, Task.category == category)
        .first()
    )
    if task:
        item = session.query(Item).filter(Item.task_id == task.id, url=url).first()
        if item:
            session.commit()
        else:
            new_item = Item(task_id=task.id, url=url, price=price)
            session.add(new_item)
            session.commit()

    else:
        new_task = Task(user_id=user_id, category=category, link=link)
        new_item = Item(task_id=task.id, url=url, price=price)
        session.add(new_task)
        session.add(new_item)
        session.commit()

    session.close()


async def fetch_with_proxy(url, proxy):
    connector = ProxyConnector.from_url(proxy)
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Referer": "https://www.avito.ru/",
    }
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url, headers=headers) as response:
            print(response)
            if response.status == 200:
                print("Request successful.")
                return await response
            else:
                print(f"Request failed with status code {response.status}")


async def fetch_without_proxy(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Referer": "https://www.avito.ru/",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            print(response)
            if response.status == 200:
                print("Request successful.")
                return await response
            else:
                print(f"Request failed with status code {response.status}")


@router.message(
    UserState.waiting_to_be_created, lambda message: message.text.startswith("http")
)
async def handle_item_link(message: types.Message, state: FSMContext, engine, db_pool):
    link = message.text
    user_id = message.from_user.id
    success = False
    if not proxies:
        res = await fetch_without_proxy(link)
    else:
        for proxy in proxies:
            print(proxy)
            sleep_time = random.uniform(1, 10)
            await asyncio.sleep(sleep_time)
            try:
                res = await fetch_with_proxy(link, proxy)
                await data_parser(res, engine, user_id, link)
                success = True
                break
            except Exception as e:
                print(f"Failed to connect to proxy {proxy}: {str(e)}")

    if not success:
        print("All proxy servers failed to connect. Trying without a proxy...")
        try:
            res = await fetch_without_proxy(link)
            await data_parser(res, engine, user_id, link)
        except Exception as e:
            print(f"Failed to connect without a proxy: {str(e)}")

    await message.answer("Sorry, but we have techn problems :(")
