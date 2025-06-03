from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Оформить заявку')],
    [KeyboardButton(text='О Пушкино Град')],
    [KeyboardButton(text='Мои промокоды')],
], resize_keyboard=True)

request_phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отправить мой номер телефона", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
