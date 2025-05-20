import os
import asyncio
from aiogram import Dispatcher, Bot

async def main():
    bot = Bot(token='')
    dp = Dispatcher()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


