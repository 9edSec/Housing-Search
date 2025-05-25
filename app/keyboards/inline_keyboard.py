from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup 


from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_houses, get_corp_house, get_floor_corp, get_apartament_floor

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

async def houses():
    all_houses = await get_houses()
    keyboard = InlineKeyboardBuilder()
    for house in all_houses:
        keyboard.add(InlineKeyboardButton(text=house.name, callback_data=f"house_{house.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()
    
async def corps(house_id):
    all_corps = await get_corp_house(house_id)
    keyboard = InlineKeyboardBuilder()
    for corp in all_corps:
        keyboard.add(InlineKeyboardButton(text=corp.name, callback_data=f"corp_{corp.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

async def floors(corp_id: int):
    all_floors = await get_floor_corp(corp_id)
    keyboard = InlineKeyboardBuilder()
    for floor in all_floors:
        keyboard.add(InlineKeyboardButton(text=f"Этаж {floor.number}", callback_data=f"floor_{floor.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()
    
async def apartaments(floor_id: int):
    all_apartaments = await get_apartament_floor(floor_id)
    keyboard = InlineKeyboardBuilder()
    for apartament in all_apartaments:
        keyboard.add(InlineKeyboardButton(text=f"№{apartament.number}", callback_data=f"apartament_{apartament.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()
    
    