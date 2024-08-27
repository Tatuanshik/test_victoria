from aiogram import Dispatcher, Bot
import asyncio
import logging
import signal
import sys
import time
#from config import BOT_TOKEN
from handler import router
import os
import json

BOT_TOKEN = os.getenv('BOT_TOKEN')

def signal_handler(signum, frame):
    print("Получилм SIGTERM, выключение...")
    sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)


while True:
    time.sleep(1)
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

