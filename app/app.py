import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI
from app.bot import bot as recap_bot

from app.configs.settings import SETTINGS


app = FastAPI()

async def main():
    print("Starting the Recap System...")
    bot = Bot(token=SETTINGS.tg_bot_token)
    dispatcher = Dispatcher(storage=MemoryStorage())

    dispatcher.include_router(recap_bot.router)

    try:
        print("The Recap System is now running. Press Ctrl+C to stop.s")
        await asyncio.gather(
            dispatcher.start_polling(bot),
        )
    finally:
        await bot.session.close()
        print("System shutdown complete.")
