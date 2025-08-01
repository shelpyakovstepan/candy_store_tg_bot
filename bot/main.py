# STDLIB
import asyncio

# THIRDPARTY
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# FIRSTPARTY
from bot.config import settings

TOKEN = settings.BOT_TOKEN


dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Привет!\n"
        "Это бот кондитерского магазина, который будет уведомлять вас о заказах и изменениях статуса их готовности!\n\n"
        "Удачных заказов!"
    )


async def main() -> None:
    await dp.start_polling(bot)
    print("Bot started")


if __name__ == "__main__":
    asyncio.run(main())
