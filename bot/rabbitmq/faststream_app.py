# THIRDPARTY
from faststream import FastStream

# FIRSTPARTY
from bot.config import get_rabbitmq_url, settings
from bot.logger import logger
from bot.main import send_message
from bot.rabbitmq.broker import broker, rabbitmq_connection

conn_url = get_rabbitmq_url()


if rabbitmq_connection():
    faststream_app = FastStream(broker)
    logger.info("Successfully connected to FastStream")
else:
    raise ConnectionError("RabbitMQ connection failed")


@broker.subscriber("messages-queue")
async def handler_send_message_for_user(message):
    """
    Слушает RabbitMQ очередь: messages-queue и выполняет функцию send_message() при получении сообщения.
    messages-queue - пользовательская очередь RabbitMQ.
    """
    await send_message(chat_id=message["chat_id"], text=message["text"])


@broker.subscriber("admin-queue")
async def handler_send_message_for_admin(message):
    """
    Слушает RabbitMQ очередь: admin-queue и выполняет функцию send_message() при получении сообщения.
    admin-queue - админская очередь RabbitMQ.
    """
    await send_message(chat_id=settings.ADMIN_ID, text=message)
