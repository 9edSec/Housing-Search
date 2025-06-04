from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


from aiogram.utils.keyboard import InlineKeyboardBuilder


select_layout_option_kb = InlineKeyboardMarkup(inline_keyboard=[
    
    [InlineKeyboardButton(text='Квартира-"линейка"', callback_data='apartment_lineika')],
    [InlineKeyboardButton(text='Квартира-"распашонка"', callback_data='apartment_open')]
    
])

select_corp_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='1', callback_data='corp_1'),
        InlineKeyboardButton(text='2', callback_data='corp_2'),
        InlineKeyboardButton(text='3', callback_data='corp_3'),
    ]
])

select_type_apartament_kb = InlineKeyboardMarkup(inline_keyboard=[
    
    [InlineKeyboardButton(text='Студия', callback_data="apartament_studio")],
    [InlineKeyboardButton(text='1 комнатная', callback_data="apartament_1")],
    [InlineKeyboardButton(text='2-х комнатная', callback_data="apartament_2")],
    [InlineKeyboardButton(text='3-х комнатная', callback_data="apartament_3")],
    
])

select_floor_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='2-5', callback_data="floor_2-5"),
        InlineKeyboardButton(text='6-10', callback_data="floor_6-10"),
        InlineKeyboardButton(text='11-16', callback_data="floor_11-16"),
    ]
])


payment_methods_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ипотека", callback_data='payment_mortgage')],
    [InlineKeyboardButton(text="Наличные", callback_data='payment_cash')],
    [InlineKeyboardButton(text="Рассрочка", callback_data='payment_installments')],
    [InlineKeyboardButton(text="Другое", callback_data='payment_other')],
])


confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить заявку', callback_data='confirm')],
    [InlineKeyboardButton(text='Отменить заявку', callback_data='cancel')]
])


