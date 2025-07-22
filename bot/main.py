# STDLIB
import asyncio

# THIRDPARTY
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# FIRSTPARTY
from bot.config import settings

TOKEN = settings.BOT_TOKEN


dp = Dispatcher()


# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!")
#
#
# @dp.message()
# async def echo_handler(message: Message) -> None:
#    try:
#        await message.send_copy(chat_id=message.chat.id)
#    except TypeError:
#        await message.answer("Nice try!")
#

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)
    print("Bot started")


if __name__ == "__main__":
    asyncio.run(main())
