from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup 


from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories

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


admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить дом', callback_data='add_house')],
    [InlineKeyboardButton(text='Добавить корпус', callback_data='add_corp')],
    [InlineKeyboardButton(text='Добавить квартиру', callback_data='add_apartament')]
])

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()
    