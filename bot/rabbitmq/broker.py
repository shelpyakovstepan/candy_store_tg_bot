# THIRDPARTY

# THIRDPARTY
from faststream.rabbit import RabbitBroker, RabbitQueue
from kombu import Connection

# FIRSTPARTY
from bot.config import get_rabbitmq_url
from bot.logger import logger

conn_url = get_rabbitmq_url()


def rabbitmq_connection():
    """Проверяет подключение к RabbitMQ."""
    try:
        with Connection(conn_url) as conn:
            conn.connect()
            logger.info("Successfully connected to RabbitMQ")
            return True
    except Exception as e:
        logger.info(f"RabbitMQ connection failed: {str(e)}")
        return False


if rabbitmq_connection():
    broker = RabbitBroker(conn_url)
    logger.info("Successfully connected to RabbitMQ")
else:
    raise ConnectionError("RabbitMQ connection failed")


async def connect_broker():
    """Подключается к RabbitMQ."""
    await broker.connect()


async def disconnect_broker():
    """Отключается от RabbitMQ."""
    await broker.stop()


async def send_message_for_candy_store(message, queue):
    """
    Отправляет сообщение в RabbitMQ.

    Args:
        message: Сообщение, которое должно быть отправлено в RabbitMQ.
        queue: Очередь, в которую должно быть отправлено сообщение.

    Returns:
        None
    """
    await broker.publish(message, queue)


messages_queue = RabbitQueue(name="messages-queue")
admin_queue = RabbitQueue(name="admin-queue")
phone_number_queue = RabbitQueue(name="phone-number-queue")
