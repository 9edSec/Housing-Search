import os
import re
import asyncio
import logging

from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command

import app.keyboards.reply_keyboard as rkb
import app.keyboards.inline_keyboard as ikb

import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def st_start(message: Message):
    await rq.set_user(message.from_user.id)  
    await message.answer('Привет, успей купить квартиру мечты в ЖК Пушкино Град!\nОформите заявку на просмотр/презентацию квартиры по кнопке "Оформить заявку"!', reply_markup=rkb.main)
    


@router.message(F.text == 'Мои промокоды')
async def promo_code(message: Message):
    photo = FSInputFile("media/navigation/promocode.png")
    await message.answer_photo(photo=photo, caption='Ваш промокод для ИНДИВИДУАЛЬНЫХ ВЫГОДНЫХ УСЛОВИЙ')


@router.message(F.text == 'О Пушкино Град')
async def about_pg(message: Message):
    chat_id = message.chat.id

    if not os.path.exists("media/about_pg/presentation.pdf"):
        logging.error(f"Файл не найден по пути: {"media/about_pg/presentation.pdf"}")
        await message.answer("Извините, файл презентации не найден на сервере.")
        return

    try:
        # --- ИЗМЕНИТЕ ЭТУ СТРОКУ ---
        # Создаем объект FSInputFile из пути к файлу
        pdf_document = FSInputFile("media/about_pg/presentation.pdf")
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