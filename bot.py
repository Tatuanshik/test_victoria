from aiogram import Dispatcher, Bot
import asyncio
import logging
#from config import BOT_TOKEN
from handler import router
import os
import json

BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def main():
    logging.info("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

