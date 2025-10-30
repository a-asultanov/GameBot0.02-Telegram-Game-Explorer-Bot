from aiogram import Bot, Dispatcher, types
import asyncio
from src.app.handlers import common, games, form
from aiogram.fsm.storage.memory import MemoryStorage
import threading
from src.app.web.api import run_flask
from src.app.web.api import create_admin_app
from src.config import Config

BOT_TOKEN = Config.BOT_TOKEN

def run_admin():
    admin_app = create_admin_app()
    admin_app.run(host="127.0.0.1", port=5001)



async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(common.router)
    dp.include_router(games.router)
    dp.include_router(form.router)
    

    # Запуск Flask в отдельном потоке
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    admin_thread = threading.Thread(target=run_admin, daemon=True)
    admin_thread.start()

    await dp.start_polling(bot)
    


if __name__ == "__main__":
    asyncio.run(main())