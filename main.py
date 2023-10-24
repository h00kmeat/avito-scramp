from config import config
import asyncio
import aiopg
import logging
from aiogram import Bot, Dispatcher
from aiopg.sa import create_engine
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy import MetaData
from config import config
from handlers import start_command, stop_command, link_handler
from sqlalchemy.ext.declarative import declarative_base
from models.all_models import User, Task, Item

Base = declarative_base()


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_routers(start_command.router, stop_command.router, link_handler.router)
    # Connect to database
    db_pool = await aiopg.create_pool(
        f"dbname={config.db_name} user={config.db_user} password={config.db_password.get_secret_value()} host={config.db_host}",
        minsize=config.db_pool_min_size,
        maxsize=config.db_pool_max_size,
    )
    engine = sa_create_engine(
        f"postgresql://{config.db_user}:{config.db_password.get_secret_value()}@{config.db_host}/{config.db_name}"
    )
    Base.metadata.create_all(bind=engine)
    await dp.start_polling(bot, db_pool=db_pool, engine=engine)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
