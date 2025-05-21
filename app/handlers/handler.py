import os
import re
import asyncio
import logging

from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import app.keyboards.reply_keyboard as rkb

router = Router()


PDF_FILE_PATH = 'media/about_pg/presentation.pdf'


class Form(StatesGroup):
    name = State()
    age = State()


def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    else:
        return None


@router.message(CommandStart())
async def st_start(message: Message):
    await message.answer('Чтобы подобрать квартиру, нажмите кнопку снизу!', reply_markup=rkb.selection_of_apartaments)


@router.message(F.text == 'Подобрать квартиру')
async def start_questionnaire_process(message: Message, state: FSMContext):
    await asyncio.sleep(2)
    await message.answer('Привет. Напиши как тебя зовут: ')
    await state.set_state(Form.name)

@router.message(F.text, Form.name)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await asyncio.sleep(2)
    await message.answer('Супер! А теперь напиши сколько тебе полных лет: ')
    await state.set_state(Form.age)

@router.message(F.text, Form.age)
async def capture_age(message: Message, state: FSMContext):
    check_age = extract_number(message.text)

    if not check_age or not (1 <= check_age <= 100):
        await message.reply('Пожалуйста, введите корректный возраст (число от 1 до 100).')
        return
    await state.update_data(age=check_age)

    data = await state.get_data()
    msg_text = (f'Вас зовут <b>{data.get("name")}</b> и вам <b>{data.get("age")}</b> лет. '
                f'Спасибо за то что ответили на мои вопросы.' )
    await message.answer(msg_text)
    await state.clear()


@router.message(F.text == 'О Пушкино Град')
async def about_pg(message: Message):
    chat_id = message.chat.id

    if not os.path.exists(PDF_FILE_PATH):
        logging.error(f"Файл не найден по пути: {PDF_FILE_PATH}")
        await message.answer("Извините, файл презентации не найден на сервере.")
        return

    try:
        # --- ИЗМЕНИТЕ ЭТУ СТРОКУ ---
        # Создаем объект FSInputFile из пути к файлу
        pdf_document = FSInputFile(PDF_FILE_PATH)
        # --- Было: pdf_document = InputFile(PDF_FILE_PATH) ---

        await message.bot.send_document(
            chat_id=chat_id,
            document=pdf_document, # Передаем объект FSInputFile
            caption="Вот информация о Пушкино Град в формате PDF! 🏡✨\nНажмите на файл, чтобы открыть."
        )

        logging.info(f"Файл 'О Пушкино Град' отправлен в чат {chat_id}")

    except Exception as e:
        logging.error(f"Ошибка при отправке файла 'О Пушкино Град': {e}")
        await message.answer("Произошла ошибка при отправке информации.")