from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
import asyncio
import random
from bs4 import BeautifulSoup
from aiohttp_proxy import ProxyConnector
from middlewares.states import UserState
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker
from models.all_models import User, Task, Item
from handlers.fetches import fetch_with_proxy, fetch_without_proxy
from handlers.parser import data_parser


proxies = []
router = Router()


@router.message(
    UserState.waiting_to_be_created, lambda message: message.text.startswith("http")
)
async def handle_item_link(
    message: types.Message, db_pool, engine, state: FSMContext
):
    link = message.text
    current_user_id = message.from_user.id
    success = False
    if not proxies:
        res = await fetch_without_proxy(link)
        
        await data_parser(res, engine, current_user_id, link, message)
    else:
        for proxy in proxies:
            print(proxy)
            try:
                sleep_time = random.randint(1, 14)
                await asyncio.sleep(sleep_time)
                res = await fetch_with_proxy(link, proxy)
                await data_parser(res, engine, current_user_id, link, message)
                success = True
                break
            except Exception as e:
                print(f"Failed to connect to proxy {proxy}: {str(e)}")

    if not success:
        print("All proxy servers failed to connect. Trying without a proxy...")
        try:
            res = await fetch_without_proxy(link)
            await data_parser(res, engine, current_user_id, link, message)
        except Exception as e:
            print(f"Failed to connect without a proxy: {str(e)}")
            await message.answer("Sorry, but we have techn problems :(")

    await message.answer(
        "Great! We will notify you when a new product becomes available"
    )
    await state.set_state(UserState.waiting_to_update)
