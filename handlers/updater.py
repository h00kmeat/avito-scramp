import asyncio
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session, sessionmaker
from models.all_models import User, Task, Item
from handlers.fetches import fetch_with_proxy, fetch_without_proxy
from handlers.parser import data_parser

async def process_updating(user_id,engine):
    while True:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter(User.user_id == str(user_id)).first()
        
        if user.is_active:
            # Выполняйте обновления

            tasks = user.tasks
            

            print("ASDASDSADASD\n")
        else:
            # Если состояние становится "неактивным", завершаем цикл
            break
        # Добавьте задержку между итерациями цикла
        await asyncio.sleep(5)