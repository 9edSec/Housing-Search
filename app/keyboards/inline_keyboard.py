from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choice_selection = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Визуальный подбор', callback_data='visual_selection')],
    [InlineKeyboardButton(text='Подбор по параметрам', callback_data='selection_by_parameters')]
])

'''Клавиатура для выбора дом 1-3'''

choice_house = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1', callback_data='house_1'),
     InlineKeyboardButton(text='2', callback_data='house_2'),
     InlineKeyboardButton(text='3', callback_data='house_3')]
])

choice_floor = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='2', callback_data='floor_2')]
])

choice_apartament = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='№4', callback_data='apartament_4')]
])

select_action =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Скачать PDF', callback_data='download_pdf')],
    [InlineKeyboardButton(text='В избранное', callback_data='to_favorites')],
    [InlineKeyboardButton(text='Оставить заявку', callback_data='leave_request')],

])