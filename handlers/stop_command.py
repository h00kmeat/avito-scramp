from aiogram.filters import Command
from aiogram import Router, F, types
from sqlalchemy.orm import Session, sessionmaker
from models.all_models import User
import asyncio
from aiogram.fsm.context import FSMContext
router = Router()


@router.message(Command("stop"))
async def cmd_stop(message: types.Message, engine, state: FSMContext):
    user_id = message.from_user.id
    session = Session(bind=engine)

    user = session.query(User).filter(User.user_id == str(user_id)).first()
    def stop():
        for task in listeners:
            task.cancel()
        loop.stop()
    if user:
        user.is_active = False
        session.commit()
        await message.answer(
            "You have been deactivated. You can activate again with /start."
        )
        
        await message.answer("Updating has been stopped.")
        
        
    else:
        await message.answer("You are not registered. Use /start to register.")

    session.close()
