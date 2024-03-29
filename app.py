from aiogram import executor
from loader import dp, bot, storage
import middlewares, handlers
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


async def on_shutdown(dispatcher):
    # Уведомляет о выключениии
    await on_shutdown_notify(dispatcher)
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
