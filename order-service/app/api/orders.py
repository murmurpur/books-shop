from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import orderOut, orderIn, orderUpdate
from app.api import db_manager
from app.api.service import is_cast_present

orders = APIRouter()

@orders.post('/', response_model=orderOut, status_code=201)
async def create_order(payload: orderIn):
    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    order_id = await db_manager.add_order(payload)
    response = {
        'id': order_id,
        **payload.dict()
    }

    return response

@orders.get('/', response_model=List[orderOut])
async def get_orders():
    return await db_manager.get_all_orders()

@orders.get('/{id}/', response_model=orderOut)
async def get_order(id: int):
    order = await db_manager.get_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    return order

@orders.put('/{id}/', response_model=orderOut)
async def update_order(id: int, payload: orderUpdate):
    order = await db_manager.get_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")

    update_data = payload.dict(exclude_unset=True)

    if 'casts_id' in update_data:
        for cast_id in payload.casts_id:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    order_in_db = orderIn(**order)

    updated_order = order_in_db.copy(update=update_data)

    return await db_manager.update_order(id, updated_order)

@orders.delete('/{id}/', response_model=None)
async def delete_order(id: int):
    order = await db_manager.get_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    return await db_manager.delete_order(id)
