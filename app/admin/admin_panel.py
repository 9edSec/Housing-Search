import asyncio
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage 
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


import app.keyboards.reply_keyboard as rkb
import app.keyboards.inline_keyboard as ikb

import app.database.requests as rq


admin_router = Router()


class AdminStates(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()



@admin_router.message(Command('admin'))
async def st_admin(message: Message, state: FSMContext):
    await message.answer('Введите ваш логин:')
    await state.set_state(AdminStates.waiting_for_login)  


@admin_router.message(AdminStates.waiting_for_login)
async def process_login(message: Message, state: FSMContext):
    login = message.text 
    
    if login == "admin":
        await message.answer('Введите ваш пароль:')
        await state.set_state(AdminStates.waiting_for_password)  
    else:
        await message.answer('Неверный логин. Попробуйте еще раз.')
        await state.finish()  


@admin_router.message(AdminStates.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    password = message.text  
   
    if password == "1234":
        await message.answer('Добро пожаловать в админ-панель!', reply_markup=ikb.admin_keyboard)
    else:
        await message.answer('Неверный пароль. Попробуйте еще раз.')
        await state.finish()  
