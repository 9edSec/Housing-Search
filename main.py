import os
import asyncio

from dotenv import load_dotenv
from aiogram import Dispatcher, Bot

from app.handlers.handler import router
from app.handlers.callback import callback_router

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(callback_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


