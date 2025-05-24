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
    waiting_for_house_name = State()


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

@admin_router.callback_query(F.data == 'add_house')
async def add_house_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название дома (категории), который хотите добавить:")
    await state.set_state(AdminStates.waiting_for_house_name) # Устанавливаем новое состояние
    await callback.answer() # Обязательно ответьте на CallbackQuery

# НОВЫЙ ОБРАБОТЧИК: Обработка ввода названия дома (категории)
@admin_router.message(AdminStates.waiting_for_house_name)
async def process_new_house_name(message: Message, state: FSMContext):
    house_name = message.text.strip() # Получаем введенное название
    if not house_name:
        await message.answer("Название дома не может быть пустым. Попробуйте еще раз.")
        return

    try:
        await rq.add_category_to_db(house_name) # Вызываем функцию для добавления в БД
        await message.answer(f"Дом (категория) '{house_name}' успешно добавлен!")
    except Exception as e:
        await message.answer(f"Произошла ошибка при добавлении дома: {e}")
    finally:
        await state.clear() # Сброс состояния
        await message.answer("Что еще хотите сделать?", reply_markup=ikb.admin_keyboard) # Возвращаем админ-меню
