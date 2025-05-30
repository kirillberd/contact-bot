import asyncio
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers.message_handlers import message_router
import logging
import sys


dp = Dispatcher()

dp.include_router(message_router)
TOKEN = getenv('BOT_TOKEN')

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())