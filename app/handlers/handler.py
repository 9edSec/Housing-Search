import os
import re
import asyncio
import logging

from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

import app.keyboards.reply_keyboard as rkb
import app.keyboards.inline_keyboard as ikb

router = Router()


@router.message(CommandStart())
async def st_start(message: Message):
    await message.answer('Чтобы подобрать квартиру, нажмите кнопку снизу!', reply_markup=rkb.selection_of_apartaments)


@router.message(F.text == 'Подобрать квартиру')
async def start_select_apartaments(message: Message):
    await message.answer('Выберите, способ подбора:', reply_markup=ikb.choice_selection)
    


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