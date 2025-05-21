from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton

selection_of_apartaments = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Подобрать квартиру')],
    [KeyboardButton(text='О Пушкино Град')],
], resize_keyboard=True)