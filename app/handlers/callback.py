from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

import app.keyboards.reply_keyboard as rkb
import app.keyboards.inline_keyboard as ikb

import app.database.requests as rq

callback_router = Router()

@callback_router.callback_query(F.data == 'visual_selection')
async def st_visual_selection(callback: CallbackQuery):
    photo = FSInputFile("media/navigation/select_house.jpg")
    await callback.message.answer_photo(photo=photo, caption="Выберите дом:", reply_markup= await ikb.houses())

@callback_router.callback_query(F.data.startswith('house_'))
async def house(callback: CallbackQuery):
    photo = FSInputFile("media/navigation/house_with_corps.png")
    await callback.answer('Вы выбрали дом')
    await callback.message.answer_photo(photo=photo, caption= 'Выберите корпус',
                                  reply_markup= await ikb.corps(callback.data.split('_')[1]))
    
@callback_router.callback_query(F.data.startswith('corp_'))
async def corp(callback: CallbackQuery):
    await callback.answer('Вы выбрали корпус')
    await callback.message.answer('Выберите этаж:', 
                                  reply_markup= await ikb.floors(callback.data.split('_')[1]))
    
@callback_router.callback_query(F.data.startswith('floor_'))
async def floor (callback: CallbackQuery):
    await callback.answer('Вы выбрали этаж')
    await callback.message.answer('Выберите № понравившейся вам квартиры:', 
                                  reply_markup= await ikb.apartaments(callback.data.split('_')[1]))
    
@callback_router.callback_query(F.data.startswith('apartament_'))
async def apartament(callback: CallbackQuery):
    photo = FSInputFile("media/navigation/apartament_4.jpg")
    apartament_data = await rq.get_apartament(callback.data.split('_')[1])
    await callback.message.answer_photo( photo=photo, caption=f'''Номер квартиры: №{apartament_data.number}\nКомнат: {apartament_data.rooms}\nЦена: {apartament_data.price}\nЦена за м2: {apartament_data.price_m2}''', reply_markup=ikb.select_action)
    

    
@callback_router.callback_query(F.data == 'to_main')
async def to_main(callback: CallbackQuery):
    await callback.message.answer('Выберите, способ подбора:', reply_markup = ikb.choice_selection)