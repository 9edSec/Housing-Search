from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from typing import Union

import app.keyboards.reply_keyboard as rkb
import app.keyboards.inline_keyboard as ikb

import app.database.requests as rq

callback_router = Router()

class ApplicationStates(StatesGroup):
    """
    Состояния для формы заявки на квартиру.
    """
    waiting_for_layout_option = State()
    waiting_for_corp = State()
    waiting_for_floor = State()
    waiting_for_section = State()
    waiting_for_apartment_number = State()
    waiting_for_payment_method = State()
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_confirmation = State()


# ID чата администратора для отправки уведомлений
ADMIN_CHAT_ID = "1747118190" # !!! ОБЯЗАТЕЛЬНО ЗАМЕНИ НА СВОЙ ID ИЛИ ID ГРУППЫ АДМИНОВ !!!

# 1. Обработчик для нажатия кнопки "Оставить заявку"-------------------------------------------------------------------------------
@callback_router.message(F.text == 'Оформить заявку')
async def start_application_form( message: Message, state: FSMContext):
    await state.set_state(ApplicationStates.waiting_for_layout_option)
    await message.answer(
        "📝 <b><i>Начинаем оформление заявки!</i></b>\n\n"
        "Пожалуйста, <b>выберите вариант планировки</b>:\n\n"
        "🏠 <b>Квартира-Линейка</b> — <i>Что это?</i>\n"
        "Это когда <b>ВСЕ ОКНА</b> (и кухни, и комнат) выходят на <b>ОДНУ СТОРОНУ</b> дома.\n\n" # Добавил \n\n для разделения
        "↔️ <b>Квартира-Распашонка</b> — <i>Что это?</i>\n" # Эмодзи, жирное название, курсив для вопроса
        "Это когда <b>ОКНА</b> выходят на <b>ДВЕ ПРОТИВОПОЛОЖНЫЕ СТОРОНЫ</b> дома." # Жирное выделение ключевых слов
        , parse_mode="HTML"
        , reply_markup=ikb.select_layout_option_kb)
     # Закрываем уведомление о нажатии на кнопку

@callback_router.callback_query(ApplicationStates.waiting_for_layout_option, F.data.startswith('apartment_'))
async def process_apartment(callback: CallbackQuery, state: FSMContext):
    
    apartment_plan = callback.data.split('_')[1] # Получаем "1", "2" и т.д.

    # Можно сделать более дружелюбное отображение
    apartment_name = {
        'lineika': 'Квартира-линейка',
        'open': 'Квартира-распашонка',
        

    }.get(apartment_plan) # Если что-то пойдет не так, покажет исходное значение

    await state.update_data(apartment_plan=apartment_name)
    await callback.answer()
    
    await state.set_state(ApplicationStates.waiting_for_floor)
    await callback.message.answer(f"Вы выбрали: {apartment_name}.\n\nОтлично! Теперь выберите этажность:",reply_markup=ikb.select_floor_kb ,parse_mode="Markdown")

'''
# 2. Обработчик для получения корпуса----------------------------------------------------------------------------------------------
@callback_router.callback_query(ApplicationStates.waiting_for_corp, F.data.startswith('corp_'))
async def process_corp(callback: CallbackQuery, state: FSMContext):
    
    corp_number = callback.data.split('_')[1] # Получаем "1", "2" и т.д.

    # Можно сделать более дружелюбное отображение
    corp_name = {
        '1': 'Корпус 1',
        '2': 'Корпус 2',
        '3': 'Корпус 3',

    }.get(corp_number) # Если что-то пойдет не так, покажет исходное значение

    await state.update_data(corp_number=corp_name)
    await callback.answer()
    
    await state.set_state(ApplicationStates.waiting_for_floor)
    await callback.message.answer(f"Вы выбрали: {corp_name}.\n\nОтлично! Теперь выберите этажность:",reply_markup=ikb.select_floor_kb ,parse_mode="Markdown")
'''

# 3. Обработчик для получения этажа------------------------------------------------------------------------------------------------------------------------------
@callback_router.callback_query(ApplicationStates.waiting_for_floor, F.data.startswith('floor_'))
async def process_floor(callback: CallbackQuery, state: FSMContext):
    floor_number = callback.data.split('_')[1]

    floor_name = {
        '2-5': 'Этаж: 2-5',
        '6-10': 'Этаж: 6-10',
        '11-16': 'Этаж: 11-16',
    }.get(floor_number) 

    await state.update_data(floor_number=floor_name)
    await state.set_state(ApplicationStates.waiting_for_apartment_number)
    await callback.message.answer(f"Вы выбрали: {floor_name}.\n\nКакой тип квартиры вас интересует?:",reply_markup=ikb.select_type_apartament_kb, parse_mode="Markdown")

# 4. Обработчик для получения номера квартиры---------------------------------------------------------------------------------------------------------------------
@callback_router.callback_query(ApplicationStates.waiting_for_apartment_number, F.data.startswith('apartament_'))
async def process_apartment_number(callback: CallbackQuery ,state: FSMContext):
    apartment_type = callback.data.split("_")[1]

    apartment_name = {
        'studio': 'Студия',
        '1': '1-комнатная',
        '2': '2-х комнатная',
        '3': '3-х комнатная',
    }.get(apartment_type) 

    await state.update_data(apartment_type=apartment_name)
    await state.set_state(ApplicationStates.waiting_for_payment_method)
    await callback.message.answer("Какой *способ оплаты* для вас предпочтителен?",
                         reply_markup=ikb.payment_methods_keyboard,
                         parse_mode="Markdown")

# 5. Обработчик для выбора способа оплаты (через callback)
@callback_router.callback_query(ApplicationStates.waiting_for_payment_method, F.data.startswith('payment_'))
async def process_payment_method(callback: CallbackQuery, state: FSMContext):
    payment_method = callback.data.split('_')[1] # Получаем "mortgage", "cash" и т.д.

    # Можно сделать более дружелюбное отображение
    method_display_name = {
        'mortgage': 'Ипотека',
        'cash': 'Наличные',
        'installments': 'Рассрочка',
        'other': 'Другое'
    }.get(payment_method, payment_method) # Если что-то пойдет не так, покажет исходное значение

    await state.update_data(payment_method=method_display_name)
    await state.set_state(ApplicationStates.waiting_for_name)
    await callback.message.answer(
        f"Вы выбрали: *{method_display_name}*.\n\n"
        "Как к вам обращаться? Пожалуйста, укажите *ваше Имя*:",
        parse_mode="Markdown"
    )
    await callback.answer()

# 6. Обработчик для получения имени
@callback_router.message(ApplicationStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    user_name = message.text
    if not user_name or len(user_name.strip()) < 2:
        await message.answer("Пожалуйста, введите ваше полное имя.")
        return

    await state.update_data(name=user_name.strip())
    await state.set_state(ApplicationStates.waiting_for_phone)
    await message.answer(
        "Отлично, *{}*!\n\n"
        "Теперь, пожалуйста, укажите ваш *контактный номер телефона* для связи.\n"
        "Вы можете нажать на кнопку ниже, чтобы отправить его автоматически, или ввести вручную:".format(user_name),
        reply_markup=rkb.request_phone_keyboard, # Клавиатура для запроса номера
        parse_mode="Markdown"
    )

# 7. Обработчик для получения телефона (и завершения)
@callback_router.message(ApplicationStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    phone_number = None
    if message.contact: # Если пользователь отправил контакт через кнопку
        phone_number = message.contact.phone_number
    elif message.text: # Если пользователь ввел номер вручную
        # Простая проверка на то, что это похоже на номер телефона
        if len(message.text) > 5 and all(c.isdigit() or c in '+-() ' for c in message.text):
            phone_number = message.text

    if not phone_number:
        await message.answer(
            "Пожалуйста, отправьте корректный номер телефона.\n"
            "Вы можете нажать на кнопку *'Отправить мой номер телефона'* или ввести его вручную.",
            reply_markup=rkb.request_phone_keyboard,
            
        )
        return

    await state.update_data(phone=phone_number)

    # Собираем все данные
    user_data = await state.get_data()

    confirmation_message = (
        f"📋 *Пожалуйста, подтвердите ваши данные:*\n\n"
        f"Имя: *{user_data.get('name', 'Не указано')}*\n"
        f"Телефон: `{user_data.get('phone', 'Не указан')}`\n"
        f"Этажность: *{user_data.get('floor_number', 'Не указан')}*\n"
        f"Тип квартиры: *{user_data.get('apartment_type', 'Не указан')}*\n"
        f"Вариант планировки *{user_data.get('apartment_plan', 'Не указан')}*\n"
        f"Предпочитаемый способ оплаты: *{user_data.get('payment_method', 'Не указан')}*\n\n"
        f"Подтверждаете ли вы эти данные?"
    )

    await message.answer(confirmation_message, reply_markup=ikb.confirmation_keyboard)
    await state.set_state(ApplicationStates.waiting_for_confirmation)
  
@callback_router.callback_query(ApplicationStates.waiting_for_confirmation, F.data == 'confirm')
async def confirm_application(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    # Формируем сообщение для админа
    admin_message_text = (
        f"🚨 *НОВАЯ ЗАЯВКА НА ПРОСМОТР/ПОКУПКУ КВАРТИРЫ!* 🚨\n\n"
        f"Пользователь ID: `{callback.from_user.id}` (@{callback.from_user.username})\n"
        f"Имя: *{user_data.get('name', 'Не указано')}*\n"
        f"Телефон: `{user_data.get('phone', 'Не указан')}`\n"
        f"-----------------------------------------\n"
        f"Этажность: *{user_data.get('floor_number', 'Не указан')}*\n"
        f"Тип квартиры: *{user_data.get('apartment_type', 'Не указан')}*\n"
        f"Вариант планировки *{user_data.get('apartment_plan', 'Не указан')}*\n"
        f"Предпочитаемый способ оплаты: *{user_data.get('payment_method', 'Не указан')}*\n\n"
        f"Свяжитесь с клиентом для дальнейших действий."
    )

    # Отправляем админу (предполагается, что bot доступен через message.bot)
    try:
        await callback.bot.send_message(ADMIN_CHAT_ID, admin_message_text)
    except Exception as e:
        print(f"Ошибка при отправке заявки админу: {e}") # Для отладки
        await callback.message.answer("Произошла ошибка при отправке заявки админу. Пожалуйста, попробуйте позже.")

    # Подтверждение для пользователя
    await callback.message.answer(
        "✅ *Заявка отправлена!* ✅\n\n"
        "Наш менеджер свяжется с вами в ближайшее время для уточнения деталей.\n"
        "Спасибо за ваш выбор!",
        reply_markup=rkb.main # Убираем клавиатуру запроса номера телефона
    )

    # Очищаем состояние FSM
    await state.clear()

@callback_router.callback_query(ApplicationStates.waiting_for_confirmation, F.data == 'cancel')
async def cancel_application(callback: CallbackQuery, state: FSMContext):
    # Очищаем состояние FSM
    await state.clear()

    await callback.message.answer(
        "😞 Жаль, что вы решили отменить заявку. Если вы передумаете, наш бот к вашим услугам!!",
        reply_markup=rkb.main # Можно вернуть основное меню или клавиатуру
    )

    await callback.answer()  # Подтверждаем, чтобы убрать значок загрузки