# /app/main.py

import asyncio
from fastapi import FastAPI

from app import rabbitmq
from app.settings import settings
from app.endpoints.order_router import order_router


app = FastAPI(title='Order Service')


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))


app.include_router(order_router, prefix='/api')
