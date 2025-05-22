from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

import app.keyboards.reply_keyboard as rkb
import app.keyboards.inline_keyboard as ikb

callback_router = Router()

@callback_router.callback_query(F.data == 'visual_selection')
async def st_visual_selection(callback: CallbackQuery):
    photo = FSInputFile("media/navigation/select_house.jpg")
    await callback.message.answer_photo(photo=photo, caption="Выберите дом от 1 до 3.", reply_markup=ikb.choice_house)

@callback_router.callback_query(F.data == 'house_1')
async def st_house(callback: CallbackQuery):
    await callback.message.answer('Выберите этаж:',reply_markup=ikb.choice_floor)

@callback_router.callback_query(F.data == 'floor_2')
async def st_floor(callback: CallbackQuery):
    photo = FSInputFile("media/navigation/floor2.jpg")
    await callback.message.answer_photo(photo=photo, caption='Выберите номер понравившейся вам квартиры:', reply_markup=ikb.choice_apartament)

@callback_router.callback_query(F.data == 'apartament_4')
async def st_apartament(callback: CallbackQuery):
    photo = FSInputFile("media/navigation/apartament_4.jpg")
    await callback.message.answer_photo(photo=photo, caption="Выберите действие:", reply_markup=ikb.select_action)