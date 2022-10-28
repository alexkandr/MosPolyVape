from os import getenv
import asyncio
from aiogram import Dispatcher, Bot
from handlers import menu, catalog, cart, address

TOKEN =  getenv('BOT_TOKEN') if (getenv('BOT_TOKEN') is not None) else open('tokens.txt', 'r').readline().strip()

async def main():

    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(menu.router)
    dp.include_router(catalog.router)
    dp.include_router(cart.router)
    dp.include_router(address.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())