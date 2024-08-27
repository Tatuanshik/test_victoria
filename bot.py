from aiogram import Bot, Dispatcher
import asyncio
import logging
import signal
import sys
import os
#from config import BOT_TOKEN

# Load the bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Import router after bot and dispatcher initialization
from handler import router
dp.include_router(router)

# Signal handler function for graceful shutdown
def signal_handler(signum, frame):
    logging.info("Received SIGTERM, shutting down...")
    # Stop polling and close the bot
    asyncio.create_task(dp.storage.close())
    asyncio.create_task(dp.storage.wait_closed())
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGTERM, signal_handler)


async def main():
    logging.info("Starting bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        # Start polling
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        # Handle shutdown on interrupt
        logging.info("Shutting down...")

if __name__ == '__main__':
    asyncio.run(main())
