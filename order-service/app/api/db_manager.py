from app.api.models import orderIn, orderOut, orderUpdate
from app.api.db import orders, database


async def add_order(payload: orderIn):
    query = orders.insert().values(**payload.dict())

    return await database.execute(query=query)

async def get_all_orders():
    query = orders.select()
    return await database.fetch_all(query=query)

async def get_order(id):
    query = orders.select(orders.c.id==id)
    return await database.fetch_one(query=query)

async def delete_order(id: int):
    query = orders.delete().where(orders.c.id==id)
    return await database.execute(query=query)

async def update_order(id: int, payload: orderIn):
    query = (
        orders
        .update()
        .where(orders.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)