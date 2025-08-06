# STDLIB
import asyncio

# THIRDPARTY
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand, Message, ReplyKeyboardRemove

# FIRSTPARTY
from bot.config import settings
from bot.logger import logger
from bot.rabbitmq.broker import (
    connect_broker,
    disconnect_broker,
    phone_number_queue,
    send_message_for_candy_store,
)

dp = Dispatcher()
bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


@dp.startup()
async def on_startup():
    await connect_broker()
    logger.info("Брокер подключен")


@dp.shutdown()
async def on_shutdown():
    await disconnect_broker()
    logger.info("Брокер отключен")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Отправляет приветственное сообщение при вызове команды /start"""
    await message.answer(
        "Привет!\n"
        "Это бот кондитерского магазина, который будет уведомлять вас о заказах и изменениях статуса их готовности!\n\n"
        "Удачных заказов!"
    )


@dp.message(Command("phone_number"))
async def request_phone(message: types.Message):
    """Предлагает добавить телефон пользователю при вызове команды /phone_number."""
    await message.answer(
        "Отправьте ваш номер для проверки:",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="📱 Отправить номер", request_contact=True)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


@dp.message(lambda message: message.contact is not None)
async def handle_contact(message: types.Message):
    """
    Принимает номер телефона пользователя и отправляет сообщение с номером в RabbitMQ
    с помощью функции send_message_for_candy_store().
    """
    phone_number = message.contact.phone_number  # pyright: ignore [reportOptionalMemberAccess]
    await message.answer(
        f"✅ Ваш номер {phone_number} принят!", reply_markup=ReplyKeyboardRemove()
    )
    await send_message_for_candy_store(
        message={"phone_number": phone_number, "chat_id": message.chat.id},
        queue=phone_number_queue,
    )


async def send_message(chat_id, text):
    """
    Отправляет сообщение пользователю через бота.

    Args:
        chat_id: Чат ID пользователя, которому должно отправиться сообщение.
        text: Текст сообщения, которое должно быть отправлено пользователю.

    Returns:
        None
    """
    await bot.send_message(chat_id=chat_id, text=text)


async def main() -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Приветствие"),
            BotCommand(command="phone_number", description="Ваш номер телефона"),
        ]
    )
    await dp.start_polling(bot)
    logger.info("Bot started")


if __name__ == "__main__":
    asyncio.run(main())
