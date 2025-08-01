# THIRDPARTY
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from kombu import Connection

# FIRSTPARTY
from bot.config import get_rabbitmq_url, settings
from bot.main import bot

conn_url = get_rabbitmq_url()


def rabbitmq_connection():
    try:
        with Connection(conn_url) as conn:
            conn.connect()
            print("Successfully connected to RabbitMQ")
            return True
    except Exception as e:
        print(f"RabbitMQ connection failed: {str(e)}")
        return False


if rabbitmq_connection():
    broker = RabbitBroker(conn_url)
    broker_app = FastStream(broker)
    print("Successfully connected to FastStream RabbitMQ")
else:
    raise ConnectionError("RabbitMQ connection failed")


@broker.subscriber("messages-queue")
async def handler_send__message_for_user(message):
    await bot.send_message(message["chat_id"], text=message["text"])


@broker.subscriber("admin-queue")
async def handler_send_message_for_admin(message):
    await bot.send_message(settings.ADMIN_ID, message)
