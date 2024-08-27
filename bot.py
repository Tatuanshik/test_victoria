from aiogram import Bot, Dispatcher
import asyncio
import logging
import signal
import sys
import os
import http.server
import socketserver
#from config import BOT_TOKEN
from threading import Thread
from handler import router

# Load the bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


# def signal_handler(signum, frame):
#     logging.info("Received SIGTERM, shutting down...")
#     asyncio.create_task(dp.storage.close())
#     asyncio.create_task(dp.storage.wait_closed())
#     sys.exit(0)


# signal.signal(signal.SIGTERM, signal_handler)

if handle_signals:
    loop = asyncio.get_running_loop()
    with suppress(NotImplementedError): 
        loop.add_signal_handler(signal.SIGTERM, self._signal_stop_polling, signal.SIGTERM)
        loop.add_signal_handler(signal.SIGINT, self._signal_stop_polling, signal.SIGINT)


def start_http_server():
    port = int(os.getenv('PORT', 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
        logging.info(f"Serving HTTP on port {port}")
        httpd.serve_forever()
        
async def main():
    logging.info("Starting bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot, handle_signals=True)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Shutting down...")

if __name__ == '__main__':
    Thread(target=start_http_server).start()
    asyncio.run(main())
