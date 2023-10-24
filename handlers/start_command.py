from aiogram.filters.command import Command
from aiogram import Router, F, types
from keyboards.for_cmd_start import get_show_create_kb
from aiogram.fsm.context import FSMContext
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker
from models.all_models import User, Task, Item
from middlewares.states import UserState

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, db_pool, engine, state: FSMContext):
    user_id = message.from_user.id

    Session = sessionmaker(bind=engine)
    session = Session()

    user = session.query(User).filter(User.user_id == str(user_id)).first()
    if user:
        user.is_active = True
        session.commit()
        await message.answer("Welcome back!")
    else:
        new_user = User(user_id=user_id, is_active=True)
        session.add(new_user)
        session.commit()

    session.close()

    await message.answer("Hi, what do u want?", reply_markup=get_show_create_kb())
    await state.set_state(UserState.choosing_buttons)


@router.callback_query(UserState.choosing_buttons, F.data.startswith("a_"))
async def callbacks_button(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    if action == "createTask":
        await callback.message.answer("Send me a link")
        print(state)
        await state.set_state(UserState.waiting_to_be_created)
        print(state)
    elif action == "showTaskList":
        pass

    await callback.answer()
