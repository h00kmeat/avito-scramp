from config import config
import asyncio
import aiopg
import logging
from aiogram import Bot, Dispatcher
from aiopg.sa import create_engine
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import Session, sessionmaker
from config import config
from handlers import start_command, stop_command, link_handler
from sqlalchemy.ext.declarative import declarative_base
from models.all_models import User, Task, Item
from handlers.start_command import cmd_start
from aiogram.fsm.storage.memory import MemoryStorage
from middlewares.data import key

global data
global current_user_id
Base = declarative_base()

async def process_task(engine):
    while True:

        Session = sessionmaker(bind=engine)
        session = Session()

      

        tasks = session.query(Task)



async def handler(dp: Dispatcher):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=config.bot_token.get_secret_value())
    dp.include_routers(start_command.router,link_handler.router,stop_command.router )

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
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    asyncio.gather(handler(dp))
    loop = asyncio.get_event_loop()
    
    try:
        loop.run_forever()
        
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
    
  
