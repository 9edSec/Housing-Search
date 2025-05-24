import os
import asyncio

from dotenv import load_dotenv
from aiogram import Dispatcher, Bot

from app.handlers.handler import router
from app.handlers.callback import callback_router
from app.admin.admin_panel import admin_router

from app.database.models import async_main

async def main():
    load_dotenv()
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(callback_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


