# /app/rabbitmq.py

import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from app.settings import settings
from app.services.delivery_service import DeliveryService
from app.repositories.db_delivery_repo import DeliveryRepo


async def process_created_order(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        DeliveryService(DeliveryRepo()).create_delivery(
            data['order_id'], data['date'], data['address'])
    except:
        traceback.print_exc()
        await msg.ack()


async def process_paid_order(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        DeliveryService(DeliveryRepo()).activate_delivery(data['id'])
    except:
        await msg.ack()
    pass


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    order_created_queue = await channel.declare_queue('laptev_order_created_queue', durable=True)
    order_paid_queue = await channel.declare_queue('laptev_order_paid_queue', durable=True)

    await order_created_queue.consume(process_created_order)
    await order_paid_queue.consume(process_paid_order)
    print('Started RabbitMQ consuming...')

    return connection
